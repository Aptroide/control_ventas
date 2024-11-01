from fastapi import HTTPException, status, APIRouter
from typing import List
from .. import schemas
from ..database import execute_query

router = APIRouter(
    prefix="/pago_parcial",
    tags=["pago_parcial"],
    responses={404: {"description": "Not found"}},
)

# -------- Pagos --------
@router.post("/{id_deuda}", status_code=status.HTTP_201_CREATED)
def registrar_pago_parcial(id_deuda: int, monto_pago: schemas.PagosDeudas):
    # Registrar el pago parcial en la tabla pagos_parciales
    query_pago = """
    INSERT INTO minimarket.pagos_parciales (id_deuda, monto_pago) 
    VALUES (%s, %s) RETURNING id_pago;
    """
    pago_id = execute_query(query_pago, (id_deuda, monto_pago.monto_pago), fetch="one")
    
    # Calcular el monto total pagado hasta ahora para la deuda
    query_total_pagado = """
    SELECT COALESCE(SUM(monto_pago), 0) AS total
    FROM minimarket.pagos_parciales
    WHERE id_deuda = %s
    """
    total_pagado = execute_query(query_total_pagado, (id_deuda,), fetch="one")
    total_pagado = total_pagado["total"]
    # # Obtener el monto original de la deuda
    query_deuda = "SELECT monto_deuda FROM minimarket.deudas WHERE id_deuda = %s"
    monto_deuda = execute_query(query_deuda, (id_deuda,), fetch="one")
    monto_deuda = monto_deuda["monto_deuda"]
    
    # Verificar si la deuda está completamente pagada
    if total_pagado >= monto_deuda:
        # Marcar la deuda como pagada y la venta como no deuda
        query_update_deuda = "UPDATE minimarket.deudas SET pagado = %s WHERE id_deuda = %s"
        query_update_venta = "UPDATE minimarket.ventas SET deuda = %s WHERE id_venta = %s"

        query_id_venta = "SELECT id_venta FROM minimarket.deudas WHERE id_deuda = %s"
        id_venta = execute_query(query_id_venta, (id_deuda,), fetch="one")

        execute_query(query_update_deuda, (True, id_deuda,), fetch="None")
        execute_query(query_update_venta, (False, id_venta["id_venta"],), fetch="None")

        return {"id_pago": pago_id["id_pago"], "message": "Pago completo registrado exitosamente", "total_pagado": total_pagado}
    else:
        return {"id_pago": pago_id["id_pago"], "message": "Pago parcial registrado exitosamente", "total_pagado": total_pagado}
