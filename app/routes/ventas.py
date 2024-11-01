from fastapi import HTTPException, status, APIRouter
from typing import List
from .. import schemas
from ..database import execute_query

router = APIRouter(
    prefix="/ventas",
    tags=["ventas"],
    responses={404: {"description": "Not found"}},
)

# -------- Ventas --------
# POST /ventas
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_ventas(new_venta: schemas.Ventas):

    query = """
    INSERT INTO minimarket.ventas (fecha, total, deuda) 
    VALUES (%s, %s, %s) RETURNING id_venta;
    """
    venta_id = execute_query(query, 
                            (new_venta.fecha, new_venta.total, new_venta.deuda), 
                            fetch="one")
    return venta_id

# GET /ventas
@router.get("/", response_model=List[schemas.Ventas])
def get_ventas():
    query = """
    SELECT id_venta, fecha, total, 
           COALESCE(deuda, FALSE) AS deuda 
    FROM minimarket.ventas
    """
    ventas = execute_query(query, (), fetch="all")
    return ventas


# GET /ventas/{id_venta}
@router.get("/{id_venta}", response_model=schemas.Ventas)
def get_ventas_by_id(id_venta: int):
    query = "SELECT * FROM minimarket.ventas WHERE id_venta = %s"
    venta = execute_query(query, 
                            (id_venta,), 
                            fetch="one")
    if not venta:
        raise HTTPException(status_code=404, detail=f"Venta with id {id_venta} not found")
    else:
        return venta
