from fastapi import FastAPI
from pydantic import ValidationError

from agents.validator import analyze_deal
from models.schemas import AnalyzeApiResponse, AnalysisError, AnalysisResponse, DealAnalysis
from tools.scraper import scrape_product

app = FastAPI()


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
