
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Producto(BaseModel):
    id_producto: Optional[int] = None  # Opcional para creación
    nombre: str
    precio: float
    codigo_qr: Optional[str] = None  # Puede ser opcional si no está disponible

class Ventas(BaseModel):
    id_venta: Optional[int] = None
    fecha: Optional[datetime] = datetime.now()
    total: float

class DetallesVentas(BaseModel):
    id_detalle: Optional[int] = None
    id_venta: int
    id_producto: int
    cantidad: int
    precio_unitario: float