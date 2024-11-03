from fastapi import HTTPException, status, APIRouter, Depends
from typing import List
from .. import schemas, oauth2
from ..database import execute_query

router = APIRouter(
    prefix="/productos",
    tags=["productos"],
    responses={404: {"description": "Not found"}},
)

# -------- Productos --------
# POST /productos
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(new_producto: schemas.Producto, current_user: int = Depends(oauth2.get_current_user)):
    query = """
    INSERT INTO minimarket.productos (nombre, precio, codigo_qr) 
    VALUES (%s, %s, %s) RETURNING id_producto;
    """
    product_id = execute_query(query, 
                            (new_producto.nombre, new_producto.precio, new_producto.codigo_qr), 
                            fetch="one")
    if "duplicate key value violates unique constraint" in str(product_id):
        raise HTTPException(status_code=409, detail="Duplicate entry: the product with the provided codigo_qr already exists.")

    return product_id

# GET /productos
@router.get("/", response_model=List[schemas.Producto])
def get_products(current_user: int = Depends(oauth2.get_current_user)):
    query = "SELECT * FROM minimarket.productos"
    products = execute_query(query, 
                            ( ), 
                            fetch="all")
    return products


# GET /productos/{id_producto}
@router.get("/{id_producto}", response_model=schemas.Producto)
def get_product_by_id(id_producto: int, current_user: int = Depends(oauth2.get_current_user)):
    query = "SELECT * FROM minimarket.productos WHERE id_producto = %s"
    product = execute_query(query, 
                            (id_producto, ), 
                            fetch="one")
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with id {id_producto} not found")
    else:
        return product
    
# GET /productos/{qr_producto}
@router.get("/qr/{qr_producto}", response_model=schemas.Producto)
def get_product_by_id(qr_producto: int, current_user: int = Depends(oauth2.get_current_user)):
    query = "SELECT * FROM minimarket.productos WHERE codigo_qr = '%s'"
    product = execute_query(query, 
                            (qr_producto, ), 
                            fetch="one")
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with qr {qr_producto} not found")
    else:
        return product
    
# PUT /productos/{id_producto}
@router.put("/{id_producto}") #, response_model=schemas.Producto
def update_product(id_producto: int, product: schemas.Producto, current_user: int = Depends(oauth2.get_current_user)):
    query = """
    UPDATE minimarket.productos
    SET nombre = %s, precio = %s, codigo_qr = %s
    WHERE id_producto = %s
    RETURNING id_producto, nombre, precio, codigo_qr;
    """
    updated_product = execute_query(query, 
                                    (product.nombre, product.precio, product.codigo_qr, id_producto), 
                                    fetch="one")

    if "duplicate key value violates unique constraint" in str(updated_product):
        raise HTTPException(status_code=409, detail="Duplicate entry: the product with the provided codigo_qr already exists.")

    if not updated_product:
        raise HTTPException(status_code=404, detail=f"Product with id {id_producto} not found")

    return updated_product
    
# DELETE /productos/{id_producto}
@router.delete("/{id_producto}")
def delete_product(id_producto: int, current_user: int = Depends(oauth2.get_current_user)):
    query = "DELETE FROM minimarket.productos WHERE id_producto = %s RETURNING id_producto, nombre;"
    deleted_product = execute_query(query, 
                                    (id_producto, ), 
                                    fetch="one")
    if not deleted_product:
        raise HTTPException(status_code=404, detail=f"Product with id {id_producto} not found")
    else:
        return {"message": f"Product with id {id_producto} deleted successfully"}