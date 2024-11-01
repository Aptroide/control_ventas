from fastapi import HTTPException, status, APIRouter
from typing import List
from .. import schemas
from ..database import execute_query

router = APIRouter(
    prefix="/deudas",
    tags=["deudas"],
    responses={404: {"description": "Not found"}},
)

# -------- Deudas --------
# POST /deuda
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_deuda(new_deuda: schemas.Deudas):

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
def get_deudas():
    query = "SELECT * FROM minimarket.deudas"
    deudas = execute_query(query, 
                            (), 
                            fetch="all")
    return deudas

# GET /deudas y id
@router.get("/{id_deuda}")
def consultar_estado_deuda(id_deuda: int):
    # Obtener los detalles de la deuda y el estado de pago
    query_deuda = """
    SELECT nombre_deudor, monto_deuda, pagado
    FROM minimarket.deudas
    WHERE id_deuda = %s
    """
    deuda = execute_query(query_deuda, (id_deuda,), fetch="one")
    
    if not deuda:
        raise HTTPException(status_code=404, detail="Deuda no encontrada")

    # Calcular el total pagado hasta ahora
    query_total_pagado = """
    SELECT COALESCE(SUM(monto_pago), 0) AS total
    FROM minimarket.pagos_parciales
    WHERE id_deuda = %s
    """
    total_pagado = execute_query(query_total_pagado, (id_deuda,), fetch="one")
    
    total_pagado = total_pagado["total"]
    deudav = deuda["monto_deuda"]

    saldo_pendiente = deudav - total_pagado
    
    # Obtener todos los pagos parciales realizados
    query_pagos_parciales = """
    SELECT id_pago, monto_pago, fecha_pago
    FROM minimarket.pagos_parciales
    WHERE id_deuda = %s
    ORDER BY fecha_pago
    """
    pagos_parciales = execute_query(query_pagos_parciales, (id_deuda,), fetch="all")
    
    return {
        "nombre_deudor": deuda["nombre_deudor"],
        "monto_deuda": deuda["monto_deuda"],
        "pagado": deuda["pagado"],
        "total_pagado": total_pagado,
        "saldo_pendiente": saldo_pendiente,
        "pagos_parciales": [
            {"id_pago": pago["id_pago"], "monto_pago": pago["monto_pago"], "fecha_pago": pago["fecha_pago"]}
            for pago in pagos_parciales
        ]
    }