from fastapi import APIRouter

from app.content.service import generate_content, regenerate_image, regenerate_caption


router = APIRouter(prefix="/content", tags=["content"])


@router.post("/generate")
def generate():
    return generate_content()


@router.post("/regenerate-image")
def regenerate_image_route():
    return regenerate_image()


@router.post("/regenerate-caption")
def regenerate_caption_route():
    return regenerate_caption()