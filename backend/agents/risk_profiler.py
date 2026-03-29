"""Risk Profiler Agent — assesses investor risk tolerance using Google Gemini."""

import json
import re

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

RISK_PROFILER_PROMPT = PromptTemplate(
    input_variables=[
        "age",
        "monthly_income",
        "monthly_expenses",
        "existing_investments",
        "risk_tolerance",
        "investment_horizon_years",
    ],
    template="""You are an expert SEBI-compliant financial risk assessment specialist.

Analyse the following investor profile and determine their risk score and category.

Investor Profile:
- Age: {age} years
- Monthly Income: ₹{monthly_income}
- Monthly Expenses: ₹{monthly_expenses}
- Monthly Surplus: ₹{monthly_surplus}
- Existing Investments: ₹{existing_investments}
- Self-Stated Risk Tolerance: {risk_tolerance}
- Investment Horizon: {investment_horizon_years} years

Instructions:
1. Calculate a risk score from 1-10 (1 = very conservative, 10 = very aggressive).
2. Assign a category: Conservative (1-3), Moderate (4-6), Aggressive (7-10).
3. Provide a one-sentence description of the investor's risk profile.

Respond ONLY with a valid JSON object in this exact format:
{{
  "score": <integer 1-10>,
  "category": "<Conservative|Moderate|Aggressive>",
  "description": "<one sentence description>"
}}""",
)


def run_risk_profiler(
    llm: ChatGoogleGenerativeAI,
    age: int,
    monthly_income: float,
    monthly_expenses: float,
    existing_investments: float,
    risk_tolerance: str,
    investment_horizon_years: int,
) -> dict:
    """Run the risk profiler agent and return a risk profile dict."""
    monthly_surplus = monthly_income - monthly_expenses

    chain = LLMChain(llm=llm, prompt=RISK_PROFILER_PROMPT)
    result = chain.invoke(
        {
            "age": age,
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "monthly_surplus": monthly_surplus,
            "existing_investments": existing_investments,
            "risk_tolerance": risk_tolerance,
            "investment_horizon_years": investment_horizon_years,
        }
    )

    raw = result.get("text", "")
    # Extract JSON from the response
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return json.loads(match.group())

    # Fallback defaults
    return {
        "score": 5,
        "category": "Moderate",
        "description": "A balanced investor comfortable with moderate market fluctuations.",
    }
