# File 08 — AI Content Generator

An MVP that generates a social media post (caption, hashtags, and an image) for a
product using an LLM and a free image-generation API.

## How it works

```
POST /content/generate
        ↓
Load dummy business/product data
        ↓
Call Groq (LLM) → caption + hashtags
        ↓
Call Pollinations → image URL
        ↓
Return combined result
```

The frontend is a single React page with one button that triggers the whole
pipeline, plus a "Regenerate image" option that swaps out just the image
without re-running the LLM call.

## Project structure

```
file08_ai_content/
├── backend/
│   ├── main.py
│   ├── .env                  # not committed — see Setup below
│   ├── requirements.txt
│   └── app/
│       └── content/
│           ├── router.py
│           ├── service.py
│           ├── llm.py
│           └── image_generator.py
└── frontend/
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
```

Create `backend/.env`:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at [console.groq.com](https://console.groq.com) — no credit card
required.

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
separately for the "Generate post" button to work.

## API endpoints

| Method | Path                       | Description                                  |
|--------|----------------------------|-----------------------------------------------|
| POST   | `/content/generate`        | Runs the full pipeline: caption, hashtags, image |
| POST   | `/content/regenerate-image`| Generates a new image only, same product/caption |

## Notes

- **Text generation** uses Groq's `openai/gpt-oss-20b` model. Free tier, rate
  limited, no billing required.
- **Image generation** uses [Pollinations.ai](https://pollinations.ai) — no
  API key needed. Each regeneration uses a random seed so a new image is
  returned each time.
- Product and business data are currently hardcoded (`DUMMY_PRODUCT`,
  `DUMMY_BUSINESS` in `service.py`) — swapping in real data is the next phase.
- `.env` is git-ignored. Never commit real API keys.

## Known limitations

- Free-tier providers can occasionally be slow, rate limited, or briefly
  unavailable (Pollinations has no uptime guarantee; Groq enforces request
  rate limits).
- The LLM is prompted to return strict JSON, but this isn't always guaranteed
  by the model — `llm.py` includes fallback parsing to handle minor
  formatting deviations.