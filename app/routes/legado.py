from ..database import execute_query
from fastapi import APIRouter

router = APIRouter()

# -------- Historial Legado --------
# GET /legado
@router.get("/legado")
def get_legado():
    query = "SELECT * FROM minimarket.historial_general_legado"
    legado = execute_query(query, 
                            (), 
                            fetch="all")
    return legado