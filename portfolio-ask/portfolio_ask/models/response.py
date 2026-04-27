from pydantic import BaseModel
from typing import List, Optional


class AnswerResponse(BaseModel):
    answer: str

    # Portfolio-related
    stock: Optional[str] = None
    value: Optional[float] = None
    total: Optional[float] = None

    # Analysis
    reasoning: Optional[str] = None
    sectors: Optional[List[str]] = None

    # News
    news: Optional[List[str]] = None