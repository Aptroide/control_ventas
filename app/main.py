from fastapi import FastAPI, HTTPException, status
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
    INSERT INTO minimarket.ventas (fecha, total) 
    VALUES (%s, %s) RETURNING id_venta;
    """
    venta_id = execute_query(query, 
                            (new_venta.fecha, new_venta.total), 
                            fetch="one")
    return venta_id

# GET /ventas
@app.get("/ventas", response_model=List[schemas.Ventas])
def get_ventas():
    query = "SELECT id_venta, fecha, total FROM minimarket.ventas"
    ventas = execute_query(query, 
                            (), 
                            fetch="all")
    return ventas

# GET /ventas/{id_venta}
@app.get("/ventas/{id_venta}", response_model=schemas.Ventas)
def get_ventas_by_id(id_venta: int):
    query = "SELECT id_venta, fecha, total FROM minimarket.ventas WHERE id_venta = %s"
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


# -------- Historial Legado --------
# GET /legado
@app.get("/legado")
def get_legado():
    query = "SELECT * FROM minimarket.historial_general_legado"
    legado = execute_query(query, 
                            (), 
                            fetch="all")
    return legado