from ..database import execute_query
from fastapi import APIRouter, Depends
from .. import oauth2

router = APIRouter()

# -------- Historial Legado --------
# GET /legado
@router.get("/legado")
def get_legado(current_user: int = Depends(oauth2.get_current_user)):
    query = "SELECT * FROM minimarket.historial_general_legado"
    legado = execute_query(query, 
                            (), 
                            fetch="all")
    return legado