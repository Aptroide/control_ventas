from fastapi import FastAPI, HTTPException, status, Body
from typing import List
from . import schemas
from .database import get_db_connection, execute_query
from .routes import products, ventas, d_ventas, deudas, pagos, legado
app = FastAPI()

app.include_router(products.router)
app.include_router(ventas.router)
app.include_router(d_ventas.router)
app.include_router(deudas.router)
app.include_router(pagos.router)
app.include_router(legado.router)
        
@app.get("/")
def root():
    return {"message": "Hello World"}