from fastapi import FastAPI

from app.content.router import router as content_router


app = FastAPI(
    title="File 08 - AI Social Content Generator",
    version="0.1.0",
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(content_router)


@app.get("/")
def root():
    return {
        "message": "File 08 AI Content Generator is running"
    }