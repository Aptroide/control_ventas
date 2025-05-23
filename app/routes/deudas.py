from fastapi import HTTPException, status, APIRouter, Depends
from typing import List
from .. import schemas, oauth2
from ..database import execute_query

router = APIRouter(
    prefix="/deudas",
    tags=["deudas"],
    responses={404: {"description": "Not found"}},
)

# -------- Deudas --------
# POST /deuda
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_deuda(new_deuda: schemas.Deudas, current_user: int = Depends(oauth2.get_current_user)):

    query = """
    INSERT INTO minimarket.deudas (id_venta, nombre_deudor, monto_deuda ) 
    VALUES (%s, %s, %s) RETURNING id_deuda;
    """
    deuda_id = execute_query(query, 
                            (new_deuda.id_venta, new_deuda.nombre_deudor, new_deuda.monto_deuda), 
                            fetch="one")
    return deuda_id

# GET /deudas
@router.get("/", response_model=List[schemas.Deudas])
def get_deudas(current_user: int = Depends(oauth2.get_current_user)):
    query = "SELECT * FROM minimarket.deudas"
    deudas = execute_query(query, 
                            (), 
                            fetch="all")
    return deudas

# GET /deudas y id
@router.get("/{id_deuda}")
def consultar_estado_deuda(id_deuda: int, current_user: int = Depends(oauth2.get_current_user)):
    # Obtener los detalles de la deuda y el estado de pago
    query_deuda = """
    SELECT *
    FROM minimarket.deudas
    WHERE id_deuda = %s
    """
    deuda = execute_query(query_deuda, (id_deuda,), fetch="one")
    
    if not deuda:
        raise HTTPException(status_code=404, detail="Deuda was not found")
    
    return deuda
