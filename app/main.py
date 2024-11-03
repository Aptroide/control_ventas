from fastapi import FastAPI
from .routes import products, ventas, d_ventas, deudas, pagos, legado, users, auth

app = FastAPI()

app.include_router(products.router)
app.include_router(ventas.router)
app.include_router(d_ventas.router)
app.include_router(deudas.router)
app.include_router(pagos.router)
app.include_router(legado.router)
app.include_router(users.router)
app.include_router(auth.router)
        
@app.get("/")
def root():
    return {"message": "Hello API"}