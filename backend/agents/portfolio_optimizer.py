"""Portfolio Optimizer Agent — recommends risk-adjusted asset allocations."""

import json
import re

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

PORTFOLIO_OPTIMIZER_PROMPT = PromptTemplate(
    input_variables=[
        "risk_score",
        "risk_category",
        "investment_amount",
        "investment_horizon_years",
        "financial_goals",
        "tax_bracket_percent",
    ],
    template="""You are an expert SEBI-compliant Indian market portfolio manager.

Create an optimal asset allocation for the investor below.

Investor Details:
- Risk Score: {risk_score}/10 ({risk_category})
- Investment Amount: ₹{investment_amount}
- Investment Horizon: {investment_horizon_years} years
- Financial Goals: {financial_goals}
- Tax Bracket: {tax_bracket_percent}%

Instructions:
1. Allocate across Equity, Debt, Gold, and Liquid categories (must sum to 100%).
2. Recommend 4-6 specific Indian market instruments (mutual funds, ETFs, PPF, etc.).
3. Tailor recommendations to the investor's goals and tax bracket.

Respond ONLY with a valid JSON object in this exact format:
{{
  "equity": "<percentage>%",
  "debt": "<percentage>%",
  "gold": "<percentage>%",
  "liquid": "<percentage>%",
  "recommended_instruments": [
    "<instrument 1>",
    "<instrument 2>",
    "<instrument 3>",
    "<instrument 4>"
  ]
}}""",
)


def run_portfolio_optimizer(
    llm: ChatGoogleGenerativeAI,
    risk_score: int,
    risk_category: str,
    investment_amount: float,
    investment_horizon_years: int,
    financial_goals: list,
    tax_bracket_percent: int,
) -> dict:
    """Run the portfolio optimizer agent and return an allocation dict."""
    goals_str = ", ".join(financial_goals)

    chain = LLMChain(llm=llm, prompt=PORTFOLIO_OPTIMIZER_PROMPT)
    result = chain.invoke(
        {
            "risk_score": risk_score,
            "risk_category": risk_category,
            "investment_amount": investment_amount,
            "investment_horizon_years": investment_horizon_years,
            "financial_goals": goals_str,
            "tax_bracket_percent": tax_bracket_percent,
        }
    )

    raw = result.get("text", "")
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return json.loads(match.group())

    # Fallback defaults based on risk score
    if risk_score <= 3:
        equity, debt, gold, liquid = "20%", "60%", "10%", "10%"
    elif risk_score <= 6:
        equity, debt, gold, liquid = "60%", "30%", "5%", "5%"
    else:
        equity, debt, gold, liquid = "80%", "10%", "5%", "5%"

    return {
        "equity": equity,
        "debt": debt,
        "gold": gold,
        "liquid": liquid,
        "recommended_instruments": [
            "Nifty 50 Index Fund",
            "ELSS Tax Saver Fund",
            "PPF",
            "Sovereign Gold Bond",
        ],
    }
