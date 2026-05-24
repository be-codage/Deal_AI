from typing import Union

from pydantic import BaseModel


class DealAnalysis(BaseModel):

    product_name: str
    original_price: str
    discounted_price: str
    estimated_discount_percentage: int

    deal_quality_rating: str
    trust_score: int

    suspicious: bool

    reasons: str
    pros: str
    cons: str

    final_verdict: str
    summary: str


class AnalysisResponse(BaseModel):

    top_deals: list[DealAnalysis]


class AnalysisError(BaseModel):

    error: str


class AnalyzeApiResponse(BaseModel):

    analysis: Union[AnalysisResponse, AnalysisError]
