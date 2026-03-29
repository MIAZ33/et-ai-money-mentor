"""Tax Optimizer Agent — recommends tax-saving instruments under Indian tax laws."""

import json
import re

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

TAX_OPTIMIZER_PROMPT = PromptTemplate(
    input_variables=[
        "age",
        "monthly_income",
        "tax_bracket_percent",
        "investment_horizon_years",
        "financial_goals",
    ],
    template="""You are an expert Indian tax planning specialist with deep knowledge of the
Income Tax Act, 1961, and SEBI regulations.

Provide tax optimisation recommendations for the investor below.

Investor Details:
- Age: {age} years
- Monthly Income: ₹{monthly_income} (Annual: ₹{annual_income})
- Tax Bracket: {tax_bracket_percent}%
- Investment Horizon: {investment_horizon_years} years
- Financial Goals: {financial_goals}

Instructions:
1. List 2-4 specific tax-saving investments under Section 80C (max ₹1,50,000/year).
2. Recommend NPS contribution under Section 80CCD(1B) (additional ₹50,000/year).
3. Calculate the estimated annual tax saving in INR.

Respond ONLY with a valid JSON object in this exact format:
{{
  "section_80C_investments": [
    "<instrument and amount>",
    "<instrument and amount>"
  ],
  "nps_deduction_80CCD": "₹50,000/year",
  "estimated_annual_tax_saving": "₹<amount>"
}}""",
)


def run_tax_optimizer(
    llm: ChatGoogleGenerativeAI,
    age: int,
    monthly_income: float,
    tax_bracket_percent: int,
    investment_horizon_years: int,
    financial_goals: list,
) -> dict:
    """Run the tax optimizer agent and return tax optimisation recommendations."""
    annual_income = monthly_income * 12
    goals_str = ", ".join(financial_goals)

    chain = LLMChain(llm=llm, prompt=TAX_OPTIMIZER_PROMPT)
    result = chain.invoke(
        {
            "age": age,
            "monthly_income": monthly_income,
            "annual_income": annual_income,
            "tax_bracket_percent": tax_bracket_percent,
            "investment_horizon_years": investment_horizon_years,
            "financial_goals": goals_str,
        }
    )

    raw = result.get("text", "")
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return json.loads(match.group())

    # Fallback defaults
    tax_saving = int(200000 * tax_bracket_percent / 100)
    return {
        "section_80C_investments": [
            "ELSS Fund: ₹1,50,000/year",
            "PPF: ₹50,000/year",
        ],
        "nps_deduction_80CCD": "₹50,000/year",
        "estimated_annual_tax_saving": f"₹{tax_saving:,}",
    }
