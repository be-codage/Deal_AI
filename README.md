# DealMind AI

AI-powered ecommerce deal analyzer. Paste a product or coupon page URL and get trust scores, discount analysis, and suspicious pricing detection.

**Live repo:** [github.com/be-codage/Deal_AI](https://github.com/be-codage/Deal_AI)
Demo website:https://dealai-byjb9cvhtxb3zrof8tsvbe.streamlit.app/

## Features

- Scrape ecommerce page content from any URL
- Analyze deals with **Groq** (Llama 3.3 70B)
- Trust score (0–100) and deal quality rating
- Flags suspicious or misleading offers
- Gradient dark-theme **Streamlit** UI
- **FastAPI** backend with Pydantic-validated responses

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| AI | Groq API (Llama 3.3 70B) |
| Scraping | BeautifulSoup + Requests |
| Validation | Pydantic |

## Project Structure

```
Deal_AI/
├── app/
│   ├── api.py           # FastAPI backend
│   └── streamlit_app.py # Streamlit UI
├── agents/
│   └── validator.py     # Groq deal analysis
├── tools/
│   └── scraper.py       # Web scraper
├── models/
│   └── schemas.py       # Pydantic response models
├── requirements.txt
└── .env                 # API keys (not committed)
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/be-codage/Deal_AI.git
cd Deal_AI
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and add your Groq API key:

```bash
cp .env.example .env
```

Edit `.env`:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com).

## Run

You need **two terminals**, both from the project root with the venv activated.

### Terminal 1 — API backend

```bash
uvicorn app.api:app --reload --host 127.0.0.1 --port 8000
```

API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Terminal 2 — Streamlit UI

```bash
streamlit run app/streamlit_app.py
```

Open the URL shown in the terminal (usually [http://localhost:8501](http://localhost:8501)).

## Usage

1. Paste an ecommerce URL (product page, coupon page, deal listing)
2. Click **Analyze Deals**
3. Review trust score, pricing, discount %, and final verdict

## API

### `GET /analyze`

**Query parameter:** `url` — the ecommerce page to analyze

**Example:**

```bash
curl "http://127.0.0.1:8000/analyze?url=https://www.example.com/deal"
```

**Success response:**

```json
{
  "analysis": {
    "top_deals": [
      {
        "product_name": "Example Product",
        "original_price": "$99.99",
        "discounted_price": "$49.99",
        "estimated_discount_percentage": 50,
        "deal_quality_rating": "Good",
        "trust_score": 85,
        "suspicious": false,
        "reasons": "...",
        "pros": "...",
        "cons": "...",
        "final_verdict": "...",
        "summary": "..."
      }
    ]
  }
}
```

**Error response:**

```json
{
  "analysis": {
    "error": "Error message here"
  }
}
```

## Deployment

This app has **two parts** that must be deployed separately:

| Service | What it runs | Suggested platform |
|---------|--------------|-------------------|
| **API** | `uvicorn app.api:app` | [Render](https://render.com) (free tier) |
| **UI** | `streamlit run app/streamlit_app.py` | [Streamlit Community Cloud](https://streamlit.io/cloud) (free) |

### Step 1 — Deploy the FastAPI backend (Render)

1. Push your code to GitHub ([be-codage/Deal_AI](https://github.com/be-codage/Deal_AI))
2. Go to [render.com](https://render.com) → **New** → **Web Service**
3. Connect your GitHub repo
4. **Settings:**
   - **Name:** `dealmind-api`
   - **Runtime:** Python
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn app.api:app --host 0.0.0.0 --port $PORT`
5. Add **Environment Variable:**
   - `GROQ_API_KEY` = your Groq key
6. Click **Create Web Service**
7. Copy your live URL, e.g. `https://dealmind-api.onrender.com`

Test it: `https://dealmind-api.onrender.com/docs`

### Step 2 — Deploy the Streamlit UI (Streamlit Cloud)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub → **New app**
3. Select repo `be-codage/Deal_AI`
4. **Main file path:** `app/streamlit_app.py`
5. Open **Advanced settings** → **Secrets** and add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
API_BASE_URL = "https://dealmind-api.onrender.com"
```

Replace `API_BASE_URL` with your Render URL from Step 1 (no trailing slash).

6. Click **Deploy**

Your app will be live at a URL like `https://deal-ai.streamlit.app`.

### Environment variables

| Variable | Where | Purpose |
|----------|-------|---------|
| `GROQ_API_KEY` | API (Render) | Groq LLM access |
| `API_BASE_URL` | UI (Streamlit secrets) | Points UI to deployed API |

### Notes

- Render free tier sleeps after inactivity — first request may take ~30 seconds to wake up
- Never commit `.env` or API keys to GitHub
- Both services need the same GitHub repo; only secrets differ per platform

## License

MIT
