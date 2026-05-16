from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.invoice import Cliente, Factura, DescripcionFactura
from app.schemas.invoice import FacturaCreate

def save_invoice_data(db: Session, invoice_data: FacturaCreate, filename: str) -> Factura:
    try:
        cliente = db.query(Cliente).filter(
            Cliente.nombre_completo == invoice_data.cliente.nombre_completo
        ).first()

        if not cliente:
            cliente = Cliente(
                nombre_completo=invoice_data.cliente.nombre_completo,
                direccion=invoice_data.cliente.direccion,
                celular=invoice_data.cliente.celular
            )
            db.add(cliente)
            db.flush() 

        factura = Factura(
            fecha=invoice_data.fecha,
            valor_total=invoice_data.valor_total,
            filename=filename,
            id_cliente=cliente.id
        )
        db.add(factura)
        db.flush() 

        detalles_db = []
        for detalle in invoice_data.detalles:
            db_detalle = DescripcionFactura(
                producto=detalle.producto,
                valor_unitario=detalle.valor_unitario,
                cantidad=detalle.cantidad,
                id_factura=factura.id
            )
            detalles_db.append(db_detalle)
    
        db.add_all(detalles_db)
        db.commit()
        db.refresh(factura)
        return factura

    except Exception as e:
        db.rollback()
        print(f"Error en BD: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al guardar la factura en la base de datos.")