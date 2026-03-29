from pydantic import BaseModel, Field
from typing import List, Optional


class WealthPlanRequest(BaseModel):
    age: int = Field(..., ge=18, le=80, description="Investor's current age")
    monthly_income: float = Field(..., gt=0, description="Monthly gross income in INR")
    monthly_expenses: float = Field(..., gt=0, description="Monthly expenses in INR")
    existing_investments: float = Field(
        default=0, ge=0, description="Current investment corpus in INR"
    )
    financial_goals: List[str] = Field(
        ..., description="List of financial goals (e.g., 'retirement at 55')"
    )
    risk_tolerance: str = Field(
        default="moderate",
        description="Risk tolerance: conservative, moderate, or aggressive",
    )
    investment_horizon_years: int = Field(
        ..., ge=1, le=40, description="Investment horizon in years"
    )
    tax_bracket_percent: Optional[int] = Field(
        default=30, ge=0, le=30, description="Income tax bracket percentage"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 32,
                "monthly_income": 150000,
                "monthly_expenses": 80000,
                "existing_investments": 500000,
                "financial_goals": ["retirement at 55", "buy a house in 5 years"],
                "risk_tolerance": "moderate",
                "investment_horizon_years": 20,
                "tax_bracket_percent": 30,
            }
        }
    }


class RiskProfileRequest(BaseModel):
    age: int = Field(..., ge=18, le=80)
    monthly_income: float = Field(..., gt=0)
    monthly_expenses: float = Field(..., gt=0)
    existing_investments: float = Field(default=0, ge=0)
    risk_tolerance: str = Field(default="moderate")
    investment_horizon_years: int = Field(..., ge=1, le=40)

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 32,
                "monthly_income": 150000,
                "monthly_expenses": 80000,
                "existing_investments": 500000,
                "risk_tolerance": "moderate",
                "investment_horizon_years": 20,
            }
        }
    }


class PortfolioRequest(BaseModel):
    risk_score: int = Field(
        ..., ge=1, le=10, description="Risk score from 1 (low) to 10 (high)"
    )
    investment_amount: float = Field(
        ..., gt=0, description="Total investment amount in INR"
    )
    investment_horizon_years: int = Field(..., ge=1, le=40)
    financial_goals: List[str] = Field(...)
    tax_bracket_percent: Optional[int] = Field(default=30, ge=0, le=30)
    age: Optional[int] = Field(
        default=None, ge=18, le=80, description="Investor age (used for tax optimisation)"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "risk_score": 6,
                "investment_amount": 1000000,
                "investment_horizon_years": 10,
                "financial_goals": ["wealth accumulation", "child education"],
                "tax_bracket_percent": 30,
                "age": 35,
            }
        }
    }


class RiskProfile(BaseModel):
    score: int
    category: str
    description: str


class PortfolioAllocation(BaseModel):
    equity: str
    debt: str
    gold: str
    liquid: str
    recommended_instruments: List[str]


class TaxOptimization(BaseModel):
    section_80C_investments: List[str]
    nps_deduction_80CCD: str
    estimated_annual_tax_saving: str


class WealthPlanResponse(BaseModel):
    risk_profile: RiskProfile
    portfolio_allocation: PortfolioAllocation
    tax_optimization: TaxOptimization
    sebi_disclaimer: str
    action_plan: List[str]


class RiskProfileResponse(BaseModel):
    risk_profile: RiskProfile
    sebi_disclaimer: str


class PortfolioResponse(BaseModel):
    portfolio_allocation: PortfolioAllocation
    tax_optimization: TaxOptimization
    sebi_disclaimer: str
    action_plan: List[str]


class HealthResponse(BaseModel):
    status: str
    version: str
    description: str
