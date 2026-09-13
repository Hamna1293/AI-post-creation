from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.content.router import router as content_router


app = FastAPI(title="File 08 - AI Content Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serves images saved by image_generator.py at http://127.0.0.1:8000/static/images/...
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(content_router)


@app.get("/")
def health_check():
    return {"status": "ok"}