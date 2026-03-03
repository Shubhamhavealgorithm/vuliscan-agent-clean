from typing import List, Literal
from pydantic import BaseModel, Field

Severity = Literal["critical", "high", "medium", "low", "info"]
Category = Literal[
    "injection","auth","secrets","crypto","rce","ssrf","path_traversal",
    "deserialization","deps","config","logging","dos","supply_chain","other",
]

class Finding(BaseModel):
    id: str
    severity: Severity
    category: Category
    file: str
    line: str
    title: str
    evidence: str
    impact: str
    recommendation: str

class ScanResult(BaseModel):
    summary: str
    overall_risk_score: int = Field(..., ge=0, le=100)
    findings: List[Finding]
