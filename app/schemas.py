from pydantic import BaseModel, EmailStr, Field, Field
from typing import List, Optional


# ---------- CONTRACT OVERVIEW ----------

class ContractOverview(BaseModel):
    contract_type: Optional[str] = ""
    scope_summary: Optional[str] = ""

    party_1: Optional[str] = ""
    party_2: Optional[str] = ""

    company_1: Optional[str] = ""
    company_2: Optional[str] = ""

    effective_date: Optional[str] = ""
    end_date: Optional[str] = ""
    duration: Optional[str] = ""

    payment_amount: Optional[str] = ""
    currency: Optional[str] = ""
    payment_terms: Optional[str] = ""

    notice_period: Optional[str] = ""
    renewal_terms: Optional[str] = ""

    jurisdiction: Optional[str] = ""
    property_address: Optional[str] = ""


# ---------- RISK BREAKDOWN ----------

class RiskBreakdown(BaseModel):
    financial_risk: int
    legal_risk: int
    flexibility_risk: int
    ip_risk: int


# ---------- RISKY CLAUSES ----------

class RiskyClause(BaseModel):
    clause_title: str
    risk_level: str
    risk_score: int

    clause_text_snippet: Optional[str] = ""

    explanation: str
    why_it_matters: str

    suggestion: str

    severity_reason: str


# ---------- CONTRACT ANALYSIS RESPONSE ----------

class ContractAnalysisResponse(BaseModel):

    contract_overview: ContractOverview

    overall_risk_score: int
    overall_risk_level: str

    summary: str

    risk_breakdown: RiskBreakdown

    risky_clauses: List[RiskyClause]

    key_concerns: List[str]

    positive_clauses: List[str]

    missing_important_clauses: List[str]

    improvement_recommendations: List[str]


# ---------- CONTRACT COMPARISON ----------

class RiskSummary(BaseModel):
    contract1_level: str
    contract2_level: str


class MissingClauses(BaseModel):
    contract1_missing: List[str]
    contract2_missing: List[str]


class Difference(BaseModel):

    topic: str

    difference_type: str

    contract1_position: str
    contract2_position: str

    risk_change: str

    risk_impact_level: str

    why_it_matters: str

    safer_option: str

    suggestion: str


class ContractComparisonResponse(BaseModel):

    contract1_risk_score: int
    contract2_risk_score: int

    risk_summary: RiskSummary

    summary: str

    better_contract: str

    key_differences: List[Difference]

    unique_risks_contract1: List[str]

    unique_risks_contract2: List[str]

    missing_important_clauses: MissingClauses

    recommendation_summary: List[str]


# ---------- NEGOTIATION EMAIL ----------

class NegotiationEmail(BaseModel):

    subject: str

    email_body: str

class UserRegister(BaseModel):
    full_name: str
    phone: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    confirm_password: str

class UserLogin(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    password: str

class GoogleToken(BaseModel):
    token: str