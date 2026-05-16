from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import List, Optional

class DetalleBase(BaseModel):
    producto: str
    valor_unitario: Decimal
    cantidad: int

class ClienteBase(BaseModel):
    nombre_completo: str
    direccion: Optional[str] = None
    celular: Optional[str] = None

class FacturaCreate(BaseModel):
    cliente: ClienteBase
    fecha: date
    valor_total: Decimal
    detalles: List[DetalleBase]

class FacturaResponse(BaseModel):
    id: int
    fecha: date
    valor_total: Decimal
    cliente: ClienteBase
    detalles: List[DetalleBase]

    class Config:
        from_attributes = True