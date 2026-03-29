"""Multi-agent workflow orchestrator for ET AI Money Mentor."""

import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import re

from agents import (
    run_risk_profiler,
    run_portfolio_optimizer,
    get_sebi_disclaimer,
    validate_compliance,
    run_tax_optimizer,
)

ACTION_PLAN_PROMPT = PromptTemplate(
    input_variables=[
        "age",
        "monthly_income",
        "monthly_expenses",
        "risk_category",
        "financial_goals",
        "portfolio_allocation",
        "tax_optimization",
    ],
    template="""You are a practical Indian personal finance coach.

Based on the investor's profile and AI-generated plan below, create a concise action plan.

Profile:
- Age: {age}
- Monthly Income: ₹{monthly_income}
- Monthly Expenses: ₹{monthly_expenses}
- Risk Category: {risk_category}
- Financial Goals: {financial_goals}

Portfolio Allocation: {portfolio_allocation}
Tax Optimisation: {tax_optimization}

Instructions:
Generate exactly 4-5 clear, actionable steps the investor should take immediately.
Each step must be a single sentence and specific to Indian markets.

Respond ONLY with a valid JSON array of strings:
["<step 1>", "<step 2>", "<step 3>", "<step 4>"]""",
)


def get_llm() -> ChatGoogleGenerativeAI:
    """Initialise and return the Google Gemini LLM."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is not set. "
            "Please add it to your /backend/.env file."
        )
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=api_key,
        temperature=0.3,
    )


def generate_wealth_plan(
    age: int,
    monthly_income: float,
    monthly_expenses: float,
    existing_investments: float,
    financial_goals: list,
    risk_tolerance: str,
    investment_horizon_years: int,
    tax_bracket_percent: int,
) -> dict:
    """
    Orchestrate all agents to generate a complete wealth plan.
    Returns a dict matching the WealthPlanResponse schema.
    """
    llm = get_llm()

    # Agent 1: Risk Profiler
    risk_profile = run_risk_profiler(
        llm=llm,
        age=age,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        existing_investments=existing_investments,
        risk_tolerance=risk_tolerance,
        investment_horizon_years=investment_horizon_years,
    )

    # Agent 2: Portfolio Optimizer
    monthly_surplus = monthly_income - monthly_expenses
    investable_amount = (monthly_surplus * 12) + existing_investments
    portfolio = run_portfolio_optimizer(
        llm=llm,
        risk_score=risk_profile["score"],
        risk_category=risk_profile["category"],
        investment_amount=investable_amount,
        investment_horizon_years=investment_horizon_years,
        financial_goals=financial_goals,
        tax_bracket_percent=tax_bracket_percent,
    )

    # Agent 3: Compliance Checker (validates portfolio)
    validate_compliance(portfolio)
    disclaimer = get_sebi_disclaimer()

    # Agent 4: Tax Optimizer
    tax_opt = run_tax_optimizer(
        llm=llm,
        age=age,
        monthly_income=monthly_income,
        tax_bracket_percent=tax_bracket_percent,
        investment_horizon_years=investment_horizon_years,
        financial_goals=financial_goals,
    )

    # Agent 5: Action Plan Generator
    action_plan = _generate_action_plan(
        llm=llm,
        age=age,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        risk_category=risk_profile["category"],
        financial_goals=financial_goals,
        portfolio=portfolio,
        tax_opt=tax_opt,
    )

    return {
        "risk_profile": risk_profile,
        "portfolio_allocation": portfolio,
        "tax_optimization": tax_opt,
        "sebi_disclaimer": disclaimer,
        "action_plan": action_plan,
    }


def _generate_action_plan(
    llm: ChatGoogleGenerativeAI,
    age: int,
    monthly_income: float,
    monthly_expenses: float,
    risk_category: str,
    financial_goals: list,
    portfolio: dict,
    tax_opt: dict,
) -> list:
    """Generate a personalised action plan using LLM."""
    chain = LLMChain(llm=llm, prompt=ACTION_PLAN_PROMPT)
    result = chain.invoke(
        {
            "age": age,
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "risk_category": risk_category,
            "financial_goals": ", ".join(financial_goals),
            "portfolio_allocation": json.dumps(portfolio),
            "tax_optimization": json.dumps(tax_opt),
        }
    )

    raw = result.get("text", "")
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if match:
        return json.loads(match.group())

    monthly_surplus = monthly_income - monthly_expenses
    emergency_fund = monthly_expenses * 6
    return [
        f"Build an emergency fund of ₹{emergency_fund:,.0f} (6 months of expenses) in a liquid fund.",
        f"Start a SIP of ₹{monthly_surplus * 0.6:,.0f}/month across recommended equity funds.",
        "Invest ₹1,50,000/year in an ELSS fund to maximise Section 80C deductions.",
        "Open an NPS account to claim an additional ₹50,000 deduction under Section 80CCD(1B).",
        "Review and rebalance your portfolio every 6 months to stay on track.",
    ]
