from fastapi import FastAPI, HTTPException, status, Body
from typing import List
from . import schemas
from .database import get_db_connection, execute_query
app = FastAPI()


        
@app.get("/")
def root():
    return {"message": "Hello World"}

# -------- Productos --------
# POST /productos
@app.post("/productos", status_code=status.HTTP_201_CREATED)
def create_product(new_producto: schemas.Producto):
    query = """
    INSERT INTO minimarket.productos (nombre, precio, codigo_qr) 
    VALUES (%s, %s, %s) RETURNING id_producto;
    """
    product_id = execute_query(query, 
                            (new_producto.nombre, new_producto.precio, new_producto.codigo_qr), 
                            fetch="one")
    return product_id

# GET /productos
@app.get("/productos", response_model=List[schemas.Producto])
# GET /productos
@app.get("/productos", response_model=List[schemas.Producto])
def get_products():
    query = "SELECT id_producto, nombre, precio, codigo_qr FROM minimarket.productos"
    products = execute_query(query, 
                            ( ), 
                            fetch="all")
    return products


# GET /productos/{id_producto}
@app.get("/productos/{id_producto}", response_model=schemas.Producto)
def get_product_by_id(id_producto: int):
    query = "SELECT id_producto, nombre, precio, codigo_qr FROM minimarket.productos WHERE id_producto = %s"
    product = execute_query(query, 
                            (id_producto, ), 
                            fetch="one")
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {id_producto} not found")
    else:
        return product


# -------- Ventas --------
# POST /ventas
@app.post("/ventas", status_code=status.HTTP_201_CREATED)
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
@app.get("/ventas", response_model=List[schemas.Ventas])
def get_ventas():
    query = """
    SELECT id_venta, fecha, total, 
           COALESCE(deuda, FALSE) AS deuda  -- Usa FALSE si deuda es NULL
    FROM minimarket.ventas
    """
    ventas = execute_query(query, (), fetch="all")
    return ventas


# GET /ventas/{id_venta}
@app.get("/ventas/{id_venta}", response_model=schemas.Ventas)
def get_ventas_by_id(id_venta: int):
    query = "SELECT * FROM minimarket.ventas WHERE id_venta = %s"
    venta = execute_query(query, 
                            (id_venta,), 
                            fetch="one")
    if not venta:
        raise HTTPException(status_code=404, detail=f"Venta with id {id_venta} not found")
    else:
        return venta

# -------- Detalles_Ventas --------
# POST /detalles_ventas
@app.post("/detalles_ventas", status_code=status.HTTP_201_CREATED)
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
@app.get("/detalles_ventas", response_model=List[schemas.DetallesVentas])
def get_detalles():
    query = "SELECT id_detalle, id_venta, id_producto, cantidad, precio_unitario, subtotal FROM minimarket.detalles_ventas"
    detalles = execute_query(query, 
                            (), 
                            fetch="all")
    return detalles


# GET /detalles_ventas/{id_detalle}
@app.get("/detalles_ventas/{id_detalle}")
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

# -------- Deudas --------
# GET /deudas
@app.get("/deudas", response_model=List[schemas.Deudas])
def get_deudas():
    query = "SELECT * FROM minimarket.deudas"
    deudas = execute_query(query, 
                            (), 
                            fetch="all")
    return deudas

# GET /deudas y id
@app.get("/deudas/{id_deuda}")
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

# -------- Pagos --------
@app.post("/pago_parcial/{id_deuda}", status_code=status.HTTP_201_CREATED)
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


# -------- Historial Legado --------
# GET /legado
@app.get("/legado")
def get_legado():
    query = "SELECT * FROM minimarket.historial_general_legado"
    legado = execute_query(query, 
                            (), 
                            fetch="all")
    return legado