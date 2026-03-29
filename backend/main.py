"""
ET AI Money Mentor — FastAPI Application
An AI-powered, SEBI-compliant wealth management mentor.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from models import (
    WealthPlanRequest,
    WealthPlanResponse,
    RiskProfileRequest,
    RiskProfileResponse,
    PortfolioRequest,
    PortfolioResponse,
    HealthResponse,
)
from orchestrator import generate_wealth_plan, get_llm
from agents import (
    run_risk_profiler,
    run_portfolio_optimizer,
    get_sebi_disclaimer,
    validate_compliance,
    run_tax_optimizer,
)

# Tax law constants (India, FY 2024-25)
SECTION_80C_LIMIT = 150_000       # ₹1,50,000 annual limit under Section 80C
NPS_80CCD_LIMIT = 50_000          # ₹50,000 additional deduction under Section 80CCD(1B)
DEFAULT_AGE = 35                  # Fallback age when not supplied in portfolio requests
EQUITY_ALLOCATION_RATIO = 0.6    # Default equity ratio for fallback action plan

app = FastAPI(
    title="ET AI Money Mentor",
    description=(
        "An AI-powered, SEBI-compliant wealth management mentor built with "
        "FastAPI, LangChain, and Google Gemini. Features a multi-agent architecture "
        "for automated, risk-adjusted financial planning."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health and status."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        description="ET AI Money Mentor is running.",
    )


@app.post(
    "/api/v1/wealth-plan",
    response_model=WealthPlanResponse,
    tags=["Wealth Planning"],
    summary="Generate a complete personalised wealth plan",
)
async def create_wealth_plan(request: WealthPlanRequest):
    """
    Generate a comprehensive, AI-powered wealth plan using multiple specialised agents:
    - **Risk Profiler**: Assesses your risk tolerance.
    - **Portfolio Optimizer**: Recommends optimal asset allocation.
    - **SEBI Compliance Checker**: Validates recommendations.
    - **Tax Optimizer**: Suggests tax-saving instruments.
    - **Action Plan Generator**: Creates actionable next steps.
    """
    try:
        plan = generate_wealth_plan(
            age=request.age,
            monthly_income=request.monthly_income,
            monthly_expenses=request.monthly_expenses,
            existing_investments=request.existing_investments,
            financial_goals=request.financial_goals,
            risk_tolerance=request.risk_tolerance,
            investment_horizon_years=request.investment_horizon_years,
            tax_bracket_percent=request.tax_bracket_percent or 30,
        )
        return WealthPlanResponse(**plan)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the wealth plan: {str(exc)}",
        ) from exc


@app.post(
    "/api/v1/risk-profile",
    response_model=RiskProfileResponse,
    tags=["Risk Assessment"],
    summary="Assess investor risk tolerance",
)
async def assess_risk_profile(request: RiskProfileRequest):
    """
    Assess the investor's risk tolerance and return a risk profile score and category.
    """
    try:
        llm = get_llm()
        risk_profile = run_risk_profiler(
            llm=llm,
            age=request.age,
            monthly_income=request.monthly_income,
            monthly_expenses=request.monthly_expenses,
            existing_investments=request.existing_investments,
            risk_tolerance=request.risk_tolerance,
            investment_horizon_years=request.investment_horizon_years,
        )
        return RiskProfileResponse(
            risk_profile=risk_profile,
            sebi_disclaimer=get_sebi_disclaimer(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while assessing the risk profile: {str(exc)}",
        ) from exc


@app.post(
    "/api/v1/portfolio",
    response_model=PortfolioResponse,
    tags=["Portfolio"],
    summary="Get an optimised portfolio allocation",
)
async def get_portfolio(request: PortfolioRequest):
    """
    Get an AI-optimised portfolio allocation and tax-saving recommendations
    based on risk score, investment amount, and financial goals.
    """
    try:
        llm = get_llm()

        # Map numeric risk score to category string
        if request.risk_score <= 3:
            risk_category = "Conservative"
        elif request.risk_score <= 6:
            risk_category = "Moderate"
        else:
            risk_category = "Aggressive"

        portfolio = run_portfolio_optimizer(
            llm=llm,
            risk_score=request.risk_score,
            risk_category=risk_category,
            investment_amount=request.investment_amount,
            investment_horizon_years=request.investment_horizon_years,
            financial_goals=request.financial_goals,
            tax_bracket_percent=request.tax_bracket_percent or 30,
        )

        validate_compliance(portfolio)

        investor_age = request.age if request.age is not None else DEFAULT_AGE
        tax_opt = run_tax_optimizer(
            llm=llm,
            age=investor_age,
            monthly_income=request.investment_amount / 12,
            tax_bracket_percent=request.tax_bracket_percent or 30,
            investment_horizon_years=request.investment_horizon_years,
            financial_goals=request.financial_goals,
        )

        equity_investment = request.investment_amount * EQUITY_ALLOCATION_RATIO
        action_plan = [
            f"Invest ₹{equity_investment:,.0f} in equity instruments as recommended.",
            f"Maximise Section 80C deductions by investing ₹{SECTION_80C_LIMIT:,}/year in ELSS funds.",
            f"Open an NPS account for an additional ₹{NPS_80CCD_LIMIT:,} deduction under Section 80CCD(1B).",
            "Review and rebalance your portfolio every 6 months.",
        ]

        return PortfolioResponse(
            portfolio_allocation=portfolio,
            tax_optimization=tax_opt,
            sebi_disclaimer=get_sebi_disclaimer(),
            action_plan=action_plan,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the portfolio: {str(exc)}",
        ) from exc
