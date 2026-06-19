from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import imagen

app = FastAPI(
    title="Comunicación de Datos · TP Integrador",
    description="API REST para digitalización de imágenes",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(imagen.router, prefix="/imagen", tags=["Digitalización de imágenes"])


@app.get("/")
def estado():
    return {"status": "ok", "servicio": "comudatos-backend"}
