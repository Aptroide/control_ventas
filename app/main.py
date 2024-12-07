from fastapi import FastAPI
from .routes import products, ventas, d_ventas, deudas, pagos, legado, users, auth, prediction
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:4200",
    config('FRONTEND_URL')
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Permite las URLs especificadas
    allow_credentials=True,
    allow_methods=["*"],            # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],            # Permite todos los encabezados
)

app.include_router(products.router)
app.include_router(ventas.router)
app.include_router(d_ventas.router)
app.include_router(deudas.router)
app.include_router(pagos.router)
app.include_router(legado.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(prediction.router)

@app.get("/")
def root():
    return {"message": "Machine Learning Final Proyect"} 