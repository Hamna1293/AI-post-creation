# File 08 — AI Content Generator

An MVP that generates a social media post (caption, hashtags, and a product
image) using a free LLM and a free image-generation service, with a polished
React frontend and the ability to regenerate the image or caption
independently.

## How it works

```
POST /content/generate
        ↓
Load dummy business/product data
        ↓
Call Groq (LLM) → caption + hashtags
        ↓
Call Pollinations, fetch image bytes server-side, save locally
        ↓
Return combined result (caption, hashtags, local image URL)
```

The frontend is a single React page: one button generates the full post, an
overlay button on the image regenerates just the picture (new random seed,
same caption), and a small icon button beside the caption regenerates just
the caption + hashtags (same image).

## Project structure

```
file08_ai_content/
├── .gitignore
├── README.md
├── backend/
│   ├── main.py
│   ├── .env                  # not committed — see Setup below
│   ├── requirements.txt
│   ├── static/
│   │   └── images/           # generated images saved here at runtime
│   └── app/
│       └── content/
│           ├── router.py
│           ├── service.py
│           ├── llm.py
│           └── image_generator.py
└── frontend/
    ├── index.html
    └── src/
        ├── App.jsx
        ├── App.css
        ├── index.css
        └── main.jsx
```

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
mkdir -p static/images
```

Create `backend/.env`:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at [console.groq.com](https://console.groq.com) — no credit
card required.

Run the server:

```bash
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:5173` by default. The backend must be running
separately for any of the buttons to work.

## API endpoints

| Method | Path                          | Description                                              |
|--------|-------------------------------|------------------------------------------------------------|
| POST   | `/content/generate`           | Full pipeline: caption, hashtags, and image                |
| POST   | `/content/regenerate-image`   | New image only (new random seed), caption unchanged         |
| POST   | `/content/regenerate-caption` | New caption + hashtags only, image unchanged                 |
| GET    | `/static/images/{filename}`   | Serves a generated image saved on the backend                |

## How images are generated

Images are **not** loaded directly from Pollinations in the browser. Instead:

1. The backend builds a Pollinations prompt URL (product description +
   style/aesthetic language, model, resolution, seed).
2. The backend fetches the image itself (`httpx`), retrying up to 3 times on
   failure and validating the response is actually image data.
3. The image is saved to `backend/static/images/` and served from the
   backend's own `/static` route.
4. The frontend only ever talks to the backend — never to Pollinations
   directly — so a Pollinations hiccup shows up as a clear backend error
   instead of a silent broken-image icon.

The image prompt currently aims for a natural, aesthetic look with a warm
citrus color palette (fitting a vitamin C serum) — see
`_build_image_prompt()` in `service.py` to adjust the style, model
(`flux`, `flux-realism`, `turbo`, etc.), or resolution.

## Notes

- **Text generation** uses Groq's `openai/gpt-oss-20b` model. Free tier, rate
  limited, no billing required. `llm.py` includes fallback JSON parsing since
  the model doesn't always return perfectly clean JSON.
- **Image generation** uses [Pollinations.ai](https://pollinations.ai) — no
  API key needed.
- Product and business data are currently hardcoded (`DUMMY_PRODUCT`,
  `DUMMY_BUSINESS` in `service.py`) — swapping in real data is the next phase.
- `.env` and `backend/static/images/` are git-ignored. Never commit real API
  keys or generated images.

## Known limitations

- Free-tier providers can occasionally be slow or rate limited. The backend
  retries image generation automatically; there's currently no retry on the
  Groq (text) call.
- Generated images accumulate in `backend/static/images/` with no cleanup —
  fine for local testing, worth addressing before any real deployment.
- Image aesthetic is tuned via prompt engineering, not a fixed template —
  expect to keep iterating on `_build_image_prompt()` as requirements change.