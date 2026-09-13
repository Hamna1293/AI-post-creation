import random
import urllib.parse


def generate_image_url(prompt: str, seed: int | None = None) -> str:
    encoded_prompt = urllib.parse.quote(prompt)

    if seed is None:
        seed = random.randint(0, 999_999)

    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"