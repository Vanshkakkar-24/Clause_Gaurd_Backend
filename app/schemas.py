from pydantic import BaseModel
from typing import List

class RiskyClause(BaseModel):
    clause_title: str
    risk_level: str
    risk_score: int
    explanation: str
    suggestion: str


class ContractAnalysisResponse(BaseModel):

    overall_risk_score: int
    summary: str
    risk_level: str

    risky_clauses: List[RiskyClause]

    key_concerns: List[str]
    safe_clauses: List[str]

    clauses: List[str]


class Difference(BaseModel):

    topic: str

    contract1: str
    contract2: str

    risk_impact: str

    recommendation: str



class ContractComparisonResponse(BaseModel):

    contract1_risk_score: int
    contract2_risk_score: int

    summary: str

    better_contract: str

    key_differences: List[Difference]

    unique_risks_contract1: List[str]

    unique_risks_contract2: List[str]


class NegotiationEmail(BaseModel):

    subject: str

    email_body: str