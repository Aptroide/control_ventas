from fastapi import HTTPException, status, APIRouter
from typing import List
from .. import schemas
from ..database import execute_query

router = APIRouter(
    prefix="/detalles_ventas",
    tags=["detalles_ventas"],
    responses={404: {"description": "Not found"}},
)

# -------- Detalles_Ventas --------
# POST /detalles_ventas
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_detalles(new_detalle: schemas.DetallesVentas):
    query = """
    INSERT INTO minimarket.detalles_ventas (id_venta, id_producto, cantidad, precio_unitario) 
    VALUES (%s, %s, %s, %s) RETURNING id_detalle;
    """
    detalle_id = execute_query(query, 
                               (new_detalle.id_venta, new_detalle.id_producto, new_detalle.cantidad, new_detalle.precio_unitario), 
                               fetch="one")

    return detalle_id


# GET /detalles_ventas
@router.get("/", response_model=List[schemas.DetallesVentas])
def get_detalles():
    query = "SELECT id_detalle, id_venta, id_producto, cantidad, precio_unitario, subtotal FROM minimarket.detalles_ventas"
    detalles = execute_query(query, 
                            (), 
                            fetch="all")
    return detalles


# GET /detalles_ventas/{id_detalle}
@router.get("/{id_detalle}")
def get_detalles_by_id(id_detalle: int):
    query = "SELECT id_detalle, id_venta, id_producto, cantidad, precio_unitario, subtotal FROM minimarket.detalles_ventas WHERE id_detalle = %s"
    detalle = execute_query(query, 
                            (id_detalle,), 
                            fetch="one")

    if not detalle:
        raise HTTPException(status_code=404,
                            detail=f"Product with id: {id_detalle} was not found")
    else:
        return detalle