import json
import os
import re

from groq import Groq
from dotenv import load_dotenv


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set in .env")

client = Groq(api_key=GROQ_API_KEY)


def _extract_json(content: str) -> dict:
    """
    Groq models sometimes wrap JSON in markdown fences or add stray text
    before/after it, even when explicitly told not to. This pulls out the
    first {...} block and parses that instead of failing outright.
    """
    content = content.strip()

    # Strip markdown code fences if present
    if content.startswith("```"):
        content = content.strip("`")
        if content.lstrip().startswith("json"):
            content = content.lstrip()[4:]
        content = content.strip()

    # Try direct parse first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Fall back to extracting the first {...} block from surrounding text
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        return json.loads(match.group(0))

    raise ValueError(f"Could not extract valid JSON from model response: {content!r}")


def generate_social_copy(product: dict, business: dict) -> dict:

    prompt = f"""
You are an AI social media content creator.

Create a promotional social media post for this business and product.

BUSINESS:
Name: {business["name"]}
Niche: {business["niche"]}

PRODUCT:
Name: {product["name"]}
Description: {product["description"]}
Category: {product["category"]}

Requirements:
- Write an engaging social media caption.
- Create exactly 5 relevant hashtags.
- Make it modern, natural, and promotional.
- Do not invent product features or claims.
- Keep the caption concise.
- Return ONLY valid JSON. No explanation, no markdown, no code fences, no text
  before or after the JSON object.

Required format:

{{
    "caption": "caption here",
    "hashtags": [
        "#hashtag1",
        "#hashtag2",
        "#hashtag3",
        "#hashtag4",
        "#hashtag5"
    ]
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You create high-quality social media marketing "
                    "content and always return valid JSON with no "
                    "surrounding text or markdown formatting."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7,
        max_tokens=400,
    )

    content = response.choices[0].message.content

    return _extract_json(content)