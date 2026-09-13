from app.content.llm import generate_social_copy
from app.content.image_generator import generate_image_url


DUMMY_BUSINESS = {
    "name": "Glow Beauty",
    "niche": "Beauty and Skincare",
}


DUMMY_PRODUCT = {
    "name": "Vitamin C Brightening Serum",
    "description": (
        "A lightweight serum designed for a fresh, "
        "radiant skincare routine."
    ),
    "category": "Skincare",
}


def _build_image_prompt() -> str:
    return f"{DUMMY_PRODUCT['name']}, {DUMMY_PRODUCT['category']}, product photography"


def generate_content() -> dict:

    social_copy = generate_social_copy(
        product=DUMMY_PRODUCT,
        business=DUMMY_BUSINESS,
    )

    image_url = generate_image_url(_build_image_prompt())

    return {
        "business": DUMMY_BUSINESS,
        "product": DUMMY_PRODUCT["name"],
        "image_url": image_url,
        "caption": social_copy["caption"],
        "hashtags": social_copy["hashtags"],
    }


def regenerate_image() -> dict:
    image_url = generate_image_url(_build_image_prompt())
    return {"image_url": image_url}