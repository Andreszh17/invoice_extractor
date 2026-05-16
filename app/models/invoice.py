from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(255), nullable=False)
    direccion = Column(String(500))
    celular = Column(String(20))

    facturas = relationship("Factura", back_populates="cliente")

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    valor_total = Column(Numeric(18, 2), nullable=False)
    filename = Column(String(255)) 
    
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    

    cliente = relationship("Cliente", back_populates="facturas")
    detalles = relationship("DescripcionFactura", back_populates="factura", cascade="all, delete-orphan")

class DescripcionFactura(Base):
    __tablename__ = "detalles_factura"

    id = Column(Integer, primary_key=True, index=True)
    producto = Column(String(255), nullable=False)
    valor_unitario = Column(Numeric(18, 2), nullable=False)
    cantidad = Column(Integer, nullable=False)
    
    id_factura = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    

    factura = relationship("Factura", back_populates="detalles")