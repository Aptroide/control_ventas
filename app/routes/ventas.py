from fastapi import HTTPException, status, APIRouter, Depends
from typing import List, Optional
from .. import schemas, oauth2
from ..database import execute_query
from datetime import datetime

router = APIRouter(
    prefix="/ventas",
    tags=["ventas"],
    responses={404: {"description": "Not found"}},
)

# -------- Ventas --------
# POST /ventas
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_ventas(new_venta: schemas.Ventas, current_user: int = Depends(oauth2.get_current_user)):

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
def get_ventas(current_user: int = Depends(oauth2.get_current_user), 
search: Optional[str] = ""):
    query = """
    SELECT id_venta, fecha, total, 
           COALESCE(deuda, FALSE) AS deuda 
    FROM minimarket.ventas
    """
    # Si se proporciona un valor de búsqueda (search), añadimos una cláusula WHERE
    if search:
        query += " WHERE fecha::date = %s::date"
    
    # Ejecuta la consulta con el parámetro de búsqueda si está presente
    ventas = execute_query(query, (search,) if search else (), fetch="all")
    
    return ventas


# GET /ventas/{id_venta}
@router.get("/{id_venta}", response_model=schemas.Ventas)
def get_ventas_by_id(id_venta: int, current_user: int = Depends(oauth2.get_current_user)):
    query = "SELECT * FROM minimarket.ventas WHERE id_venta = %s"
    venta = execute_query(query, 
                            (id_venta,), 
                            fetch="one")
    if not venta:
        raise HTTPException(status_code=404, detail=f"Venta with id {id_venta} not found")
    else:
        return venta
