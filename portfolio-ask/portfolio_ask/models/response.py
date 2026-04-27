from pydantic import BaseModel
from typing import List, Optional


class ResponseModel(BaseModel):
    answer: str
    status: str
    reason: Optional[str]
    sources: List[str]