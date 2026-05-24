from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import ValidationError

from agents.validator import analyze_deal
from models.schemas import AnalyzeApiResponse, AnalysisError, AnalysisResponse, DealAnalysis
from tools.scraper import scrape_product

app = FastAPI(
    title="DealMind AI API",
    description="Ecommerce deal analysis backend. Use /docs to test endpoints.",
)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DealMind AI API</title>
        <style>
            body { font-family: system-ui, sans-serif; max-width: 640px; margin: 60px auto; padding: 0 20px; }
            h1 { color: #5B8CFF; }
            a { color: #FF4DCA; }
            code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>DealMind AI — API</h1>
        <p>This URL is the <strong>backend API</strong>, not the visual analyzer UI.</p>
        <ul>
            <li><a href="/docs">API docs (Swagger)</a> — test <code>/analyze</code> here</li>
            <li>Example: <code>/analyze?url=https://example.com/product</code></li>
        </ul>
        <p>The gradient analyzer page is the <strong>Streamlit app</strong>.
        Deploy it on <a href="https://share.streamlit.io">Streamlit Cloud</a>
        and set <code>API_BASE_URL</code> to this server URL.</p>
    </body>
    </html>
    """


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/analyze", response_model=AnalyzeApiResponse)
def analyze(url: str):

    content = scrape_product(url)
    result = analyze_deal(content)

    if "error" in result:
        return {"analysis": AnalysisError(error=result["error"])}

    deals = result["top_deals"] if "top_deals" in result else [result]

    try:
        top_deals = [DealAnalysis.model_validate(deal) for deal in deals]
    except ValidationError as e:
        return {"analysis": AnalysisError(error=str(e))}

    return {"analysis": AnalysisResponse(top_deals=top_deals)}
