
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
    deuda: Optional[bool] = False

class DetallesVentas(BaseModel):
    id_detalle: Optional[int] = None
    id_venta: int
    id_producto: int
    cantidad: int
    precio_unitario: float

class Deudas(BaseModel):
    id_deuda: Optional[int] = None
    id_venta: int
    nombre_deudor: str
    monto_deuda: float
    fecha_deuda: Optional[datetime] = datetime.now()
    pagado: Optional[bool] = False

class PagosDeudas(BaseModel):
    id_pago: Optional[int] = None
    id_deuda: Optional[int] = None
    monto_pago: float
    fecha_pago: Optional[datetime] = datetime.now()

class User(BaseModel):
    username: str
    password: str
    created_at: Optional[datetime] = datetime.now()

class UserOut(BaseModel):
    id_user: int
    username: str
    created_at: Optional[datetime] = datetime.now()

class UserLogin(BaseModel):
    username: str
    password: str

