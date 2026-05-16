from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from app.core.database import get_db
from app.schemas.invoice import FacturaCreate, FacturaResponse
from app.services.llm_service import extract_invoice_data
from app.services.db_service import save_invoice_data
from app.models.invoice import Factura

router = APIRouter()

@router.post("/upload-invoice/", response_model=FacturaResponse, summary="Procesar y guardar factura")
async def upload_and_process_invoice(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Formato no válido. Sube un PDF o Imagen.")

    extracted_data_dict = await extract_invoice_data(file)

    try:
        invoice_data = FacturaCreate(**extracted_data_dict)
    except Exception as e:
        print(f"Error de validación Pydantic: {e}")
        raise HTTPException(status_code=422, detail="La IA devolvió datos incompletos o mal formateados.")

    try:
        factura_guardada = save_invoice_data(db=db, invoice_data=invoice_data, filename=file.filename)
        return factura_guardada
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error interno al guardar en la base de datos.")

@router.get("/invoices/", response_model=List[FacturaResponse], summary="Listar todas las facturas")
def get_all_invoices(db: Session = Depends(get_db)):
    facturas = db.query(Factura).all()
    return facturas