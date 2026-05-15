from pydantic import BaseModel
from typing import List, Dict, Any


class ReportResponse(BaseModel):

    report_id: int

    verdict: str
    risk_score: int

    explanation: List[str]

    indicators: Dict[str, Any]

    raw_email: str