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
    # Obtener el monto original de la deuda
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


# GET /pagos
@router.get("/", response_model=List[schemas.PagosDeudas])
def get_pagos_parciales():
    query = "SELECT * FROM minimarket.pagos_parciales"
    pagos = execute_query(query, (), fetch="all")
    return pagos

# GET /pagos y id
@router.get("/{id_pago}")
def get_pago_parcial_by_id(id_pago: int):
    query = "SELECT * FROM minimarket.pagos_parciales WHERE id_pago = %s"
    pago = execute_query(query, (id_pago,), fetch="one")
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago

# PUT /pagos y id
@router.put("/{id_pago}")
def update_pago_parcial(id_pago: int, monto_pago: schemas.PagosDeudas):
    # Actualizar el monto del pago parcial
    query = """
    UPDATE minimarket.pagos_parciales SET monto_pago = %s 
    WHERE id_pago = %s RETURNING id_pago, id_deuda;
    """
    pago_id = execute_query(query, (monto_pago.monto_pago, id_pago), fetch="one")
    if not pago_id:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    id_deuda = pago_id["id_deuda"]

    # Calcular el monto total pagado hasta ahora para la deuda
    query_total_pagado = """
    SELECT COALESCE(SUM(monto_pago), 0) AS total
    FROM minimarket.pagos_parciales
    WHERE id_deuda = %s
    """
    total_pagado = execute_query(query_total_pagado, (id_deuda,), fetch="one")
    total_pagado = total_pagado["total"]
    # Obtener el monto original de la deuda
    query_deuda = "SELECT monto_deuda, id_venta FROM minimarket.deudas WHERE id_deuda = %s"
    monto_deuda = execute_query(query_deuda, (id_deuda,), fetch="one")
    monto_deuda = monto_deuda["monto_deuda"]
    
    # Obtener id de la venta
    query_id_venta = "SELECT id_venta FROM minimarket.deudas WHERE id_deuda = %s"
    id_venta = execute_query(query_id_venta, (id_deuda,), fetch="one")

    # Verificar si la deuda está completamente pagada
    if total_pagado >= monto_deuda:
        # Marcar la deuda como pagada y la venta como no deuda
        query_update_deuda = "UPDATE minimarket.deudas SET pagado = %s WHERE id_deuda = %s"
        query_update_venta = "UPDATE minimarket.ventas SET deuda = %s WHERE id_venta = %s"
        execute_query(query_update_deuda, (True, id_deuda,), fetch="None")
        execute_query(query_update_venta, (False, id_venta["id_venta"],), fetch="None")
        if total_pagado == monto_deuda:
            return {"id_pago": pago_id["id_pago"], "message": "Pago completo actualizado exitosamente", "total_pagado": total_pagado}
        else:
            return {"id_pago": pago_id["id_pago"], "message": "Pago parcial actualizado exitosamente", "total_pagado": total_pagado}

    elif total_pagado < monto_deuda:
        # Marcar la deuda como no pagada y la venta como deuda
        query_update_deuda = "UPDATE minimarket.deudas SET pagado = %s WHERE id_deuda = %s"
        query_update_venta = "UPDATE minimarket.ventas SET deuda = %s WHERE id_venta = %s"
        execute_query(query_update_deuda, (False, id_deuda,), fetch="None")
        execute_query(query_update_venta, (True, id_venta["id_venta"],), fetch="None")

        return {"id_pago": pago_id["id_pago"], "message": "Pago parcial actualizado exitosamente", "total_pagado": total_pagado}