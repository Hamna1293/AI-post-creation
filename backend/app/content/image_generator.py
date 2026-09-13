import os
import random
import time
import urllib.parse
import uuid

import httpx


STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "images")
os.makedirs(STATIC_DIR, exist_ok=True)

MAX_RETRIES = 3
TIMEOUT_SECONDS = 30


def _build_pollinations_url(
    prompt: str,
    seed: int,
    width: int,
    height: int,
    model: str,
) -> str:
    encoded_prompt = urllib.parse.quote(prompt)

    params = {
        "model": model,
        "width": width,
        "height": height,
        "seed": seed,
        "nologo": "true",
        "enhance": "true",
    }
    query_string = urllib.parse.urlencode(params)

    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?{query_string}"


def generate_image_url(
    prompt: str,
    seed: int | None = None,
    width: int = 1024,
    height: int = 1280,
    model: str = "flux",
) -> str:
    """
    Fetches the image from Pollinations server-side (with retries), saves it
    locally, and returns a URL pointing at OUR OWN server instead of
    Pollinations directly. This means:
      - the browser never depends on Pollinations being reachable
      - we can retry transient failures before ever responding to the frontend
      - we can validate the response is actually image data, not an error page
    """
    if seed is None:
        seed = random.randint(0, 999_999)

    source_url = _build_pollinations_url(prompt, seed, width, height, model)

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = httpx.get(source_url, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                raise ValueError(f"Expected an image, got content-type: {content_type}")

            filename = f"{uuid.uuid4().hex}.jpg"
            filepath = os.path.join(STATIC_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            return f"/static/images/{filename}"

        except (httpx.HTTPError, ValueError) as e:
            last_error = e
            if attempt < MAX_RETRIES:
                time.sleep(1.5 * attempt)  # brief backoff before retrying
            continue

    raise RuntimeError(
        f"Failed to generate image after {MAX_RETRIES} attempts: {last_error}"
    )