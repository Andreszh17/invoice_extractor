import base64
import json
import os
from fastapi import UploadFile, HTTPException
from anthropic import AsyncAnthropic

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


INVOICE_EXTRACTION_TOOL = {
    "name": "extraer_datos_factura",
    "description": "Extrae la información clave de una factura de servicios o compras.",
    "input_schema": {
        "type": "object",
        "properties": {
            "cliente": {
                "type": "object",
                "properties": {
                    "nombre_completo": {"type": "string", "description": "Nombre de la persona o empresa facturada."},
                    "direccion": {"type": "string", "description": "Dirección física, si aparece."},
                    "celular": {"type": "string", "description": "Teléfono o celular, si aparece."}
                },
                "required": ["nombre_completo"]
            },
            "fecha": {
                "type": "string", 
                "description": "Fecha de emisión de la factura ESTRICTAMENTE en formato YYYY-MM-DD."
            },
            "valor_total": {
                "type": "number", 
                "description": "El valor total final a pagar en la factura, sin símbolos de moneda."
            },
            "detalles": {
                "type": "array",
                "description": "Lista de todos los productos o servicios cobrados en la factura.",
                "items": {
                    "type": "object",
                    "properties": {
                        "producto": {"type": "string", "description": "Nombre o descripción del producto/servicio."},
                        "valor_unitario": {"type": "number", "description": "Precio por unidad."},
                        "cantidad": {"type": "integer", "description": "Cantidad adquirida."}
                    },
                    "required": ["producto", "valor_unitario", "cantidad"]
                }
            }
        },
        "required": ["cliente", "fecha", "valor_total", "detalles"]
    }
}

async def extract_invoice_data(file: UploadFile) -> dict:
    try:
        file_bytes = await file.read()
        base64_file = base64.b64encode(file_bytes).decode("utf-8")
        media_type = file.content_type

        if media_type == "application/pdf":
            document_block = {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": base64_file
                }
            }
        elif media_type in ["image/jpeg", "image/png", "image/webp"]:
            document_block = {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64_file
                }
            }
        else:
            raise HTTPException(status_code=400, detail="Formato no soportado. Sube un PDF, JPG o PNG.")

        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            temperature=0.0, 
            system="Eres un experto contable y de extracción de datos. Tu único trabajo es leer el documento proporcionado y extraer los datos solicitados utilizando la herramienta proveída. Si algún dato no está explícito (como celular o dirección), omítelo, pero NUNCA inventes información.",
            tools=[INVOICE_EXTRACTION_TOOL],
            tool_choice={"type": "tool", "name": "extraer_datos_factura"}, 
            messages=[
                {
                    "role": "user",
                    "content": [
                        document_block,
                        {"type": "text", "text": "Por favor, extrae los datos de esta factura."}
                    ]
                }
            ]
        )

        for content in response.content:
            if content.type == 'tool_use' and content.name == 'extraer_datos_factura':

                return content.input
                
        raise HTTPException(status_code=500, detail="El modelo no pudo extraer la información.")

    except Exception as e:

        print(f"Error en LLM Service: {str(e)}")
        raise HTTPException(status_code=500, detail="Error procesando el documento con el LLM.")
    
    finally:
        await file.seek(0)