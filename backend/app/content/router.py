from fastapi import APIRouter

from app.content.service import generate_content, regenerate_image


router = APIRouter(prefix="/content", tags=["content"])


@router.post("/generate")
def generate():
    return generate_content()


@router.post("/regenerate-image")
def regenerate():
    return regenerate_image()