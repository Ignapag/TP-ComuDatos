# Comunicación de Datos 2025 · TP Integrador · Comisión S33

Aplicación cliente-servidor (React + FastAPI) que implementa la siguiente propuesta del TP:

1. **Digitalización de imágenes**: muestreo (resolución) y cuantización de color (bits por canal), con comparación visual y compresión del resultado.

## Integrantes

- Santoro, José Joaquín 
- Aramburu, Tomás 
- Pagotto, Ignacio
- Leguizamón, Nicolás 

## Arquitectura

```
frontend (React + Vite)  <-- HTTP/JSON -->  backend (FastAPI / Python)
```

- **frontend/**: SPA en React. Consume la API vía `fetch`.
- **backend/**: API REST en FastAPI con endpoint `/imagen/procesar`.

## Demo en vivo (instrumento de ejecución — recomendado)

La app ya está desplegada y corriendo; no hace falta instalar nada para probarla:

- Frontend: https://tp-comu-datos.vercel.app/
- Backend (Swagger): https://comudatos-backend.onrender.com/docs

> Nota: el backend está en el plan free de Render; si lleva varios minutos sin uso, la primera petición puede demorar ~30-50s mientras el servicio se reactiva.

## Ejecución local (opcional, solo para desarrollo)

Pensado para modificar el código y probarlo antes de subirlo; no es necesario para usar la app.

### Requisitos previos

- [Node.js](https://nodejs.org/) 18+ y npm (para el frontend)
- [Python](https://www.python.org/) 3.10+ (para el backend)

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

La API queda disponible en `http://localhost:8000`. La documentación interactiva (Swagger) está en `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

La aplicación queda disponible en `http://localhost:5173`. Por defecto se conecta a `http://localhost:8000`; si el backend corre en otra URL, copiar `.env.example` a `.env` y ajustar `VITE_API_URL`.

## Cómo se desplegó (referencia)

Pasos seguidos para publicar esta instancia en vivo, por si hace falta redeployar o crear una nueva:

1. **Backend en Render**: cuenta en [render.com](https://render.com) → conectar el repo de GitHub → "New +" → "Blueprint". Render detecta `render.yaml` (en la raíz) y configura automáticamente root directory `backend`, build command `pip install -r requirements.txt` y start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
2. **Frontend en Vercel**: cuenta en [vercel.com](https://vercel.com) → conectar el mismo repo → root directory `frontend` (Vercel detecta Vite solo). En "Environment Variables" agregar `VITE_API_URL` con la URL del backend de Render (sin barra final).

## Endpoints principales

| Método | Endpoint                 | Descripción                                              |
|--------|---------------------------|-----------------------------------------------------------|
| POST   | `/imagen/procesar`        | Recibe una imagen (multipart) + resolución + bits/canal y devuelve original y digitalizada en base64, junto con tamaños de archivo. |

## Estructura del proyecto

```
backend/
  app/
    main.py                 # App FastAPI, CORS, routers
    routers/
      imagen.py              # Endpoint /imagen/procesar
    services/
      imagen_service.py       # Muestreo, cuantización, compresión (Pillow)
    models/
      schemas.py               # Modelos Pydantic (request/response)
  requirements.txt

frontend/
  index.html
  src/
    main.jsx
    App.jsx / App.css
    api/client.js              # Llamadas fetch a la API
    components/
      ImagenDigitalizador/
        ImagenDigitalizador.jsx / .css
        Controles.jsx
        ComparadorImagenes.jsx
    styles/
      index.css                # Estilos globales / variables
      shared.css                # Componentes reutilizables (botones, chips, panel)
```

## Notas de implementación

- El muestreo reduce la imagen a una grilla de NxN (manteniendo relación de aspecto) usando interpolación NEAREST, lo que produce el efecto de "pixelado" visible al comparar con el original.
- La cuantización de bits por canal soporta 1 bit (blanco y negro), 8 bits (paleta adaptativa de 256 colores) y 24 bits (color verdadero, sin reducción).
- La compresión del resultado, cuando está activada, exporta la imagen como JPEG con calidad reducida; si no, como PNG.
