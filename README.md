# 🤑 ET AI Money Mentor

**An AI-powered, SEBI-compliant wealth management mentor** built with FastAPI, LangChain, and Google Gemini. Features a multi-agent architecture for automated, risk-adjusted financial planning tailored to the Indian market.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-orange.svg)](https://python.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Pro-red.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Features

- **Multi-Agent Architecture**: Specialized AI agents work in concert to deliver holistic financial advice.
  - 🔍 **Risk Profiler Agent**: Assesses your risk tolerance from your financial profile.
  - 📊 **Portfolio Optimizer Agent**: Recommends risk-adjusted asset allocations (Equity, Debt, Gold, etc.).
  - ✅ **SEBI Compliance Agent**: Ensures all recommendations adhere to SEBI regulations.
  - 💰 **Tax Optimizer Agent**: Suggests tax-saving instruments (ELSS, NPS, PPF) under Indian tax laws.
- **Google Gemini 1.5 Pro** powered reasoning for nuanced, context-aware financial advice.
- **RESTful API** with interactive Swagger UI documentation.
- **SEBI-Compliant Disclaimers** embedded in every response.
- **Structured JSON Responses** for easy frontend integration.

---

## 🏗️ Architecture

```
et-ai-money-mentor/
│
├── backend/
│   ├── main.py                  # FastAPI application & API routes
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── risk_profiler.py     # Risk tolerance assessment agent
│   │   ├── portfolio_optimizer.py # Asset allocation optimizer agent
│   │   ├── compliance_checker.py  # SEBI compliance verification agent
│   │   └── tax_optimizer.py     # Tax-saving recommendations agent
│   ├── models.py                # Pydantic request/response models
│   ├── orchestrator.py          # Multi-agent workflow orchestrator
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment variable template
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- A Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### 1. Clone the Repository

```bash
git clone https://github.com/MIAZ33/et-ai-money-mentor.git
cd et-ai-money-mentor
```

### 2. Set Up Your Environment Variables

Create a `.env` file in the `/backend` directory and add your Google Gemini API key:

```bash
cd backend
cp .env.example .env
```

Then open `.env` and fill in your key:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### 3. Install Dependencies

```bash
# From the /backend directory
pip install -r requirements.txt
```

### 4. 🔥 Fire Up the Engine

```bash
# From the /backend directory
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You should see output like:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

### 5. 🧪 Test the API

Navigate to **[http://localhost:8000/docs](http://localhost:8000/docs)** in your browser to interact with the **Swagger UI** and generate a wealth plan!

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/wealth-plan` | Generate a complete personalised wealth plan |
| `POST` | `/api/v1/risk-profile` | Assess investor risk tolerance |
| `POST` | `/api/v1/portfolio` | Get optimised portfolio allocation |
| `GET`  | `/health` | API health check |
| `GET`  | `/docs` | Interactive Swagger UI |

---

## 📋 Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/wealth-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 32,
    "monthly_income": 150000,
    "monthly_expenses": 80000,
    "existing_investments": 500000,
    "financial_goals": ["retirement at 55", "buy a house in 5 years"],
    "risk_tolerance": "moderate",
    "investment_horizon_years": 20,
    "tax_bracket_percent": 30
  }'
```

## 📋 Example Response

```json
{
  "risk_profile": {
    "score": 6,
    "category": "Moderate",
    "description": "Comfortable with some market volatility for higher long-term returns."
  },
  "portfolio_allocation": {
    "equity": "60%",
    "debt": "30%",
    "gold": "5%",
    "liquid": "5%",
    "recommended_instruments": [
      "Nifty 50 Index Fund",
      "ELSS (Tax Saver) Fund",
      "PPF",
      "Sovereign Gold Bond"
    ]
  },
  "tax_optimization": {
    "section_80C_investments": ["ELSS Fund: ₹1,50,000/year", "PPF: ₹50,000/year"],
    "nps_deduction_80CCD": "₹50,000/year",
    "estimated_annual_tax_saving": "₹75,000"
  },
  "sebi_disclaimer": "This is an AI-generated advisory for informational purposes only and does not constitute investment advice as defined by SEBI. Please consult a SEBI-registered investment advisor before making investment decisions.",
  "action_plan": [
    "Start a SIP of ₹30,000/month in a Nifty 50 Index Fund.",
    "Invest ₹1,50,000/year in an ELSS fund before March 31st.",
    "Open an NPS account to claim additional ₹50,000 deduction under 80CCD(1B).",
    "Build an emergency fund of ₹4,80,000 (6 months of expenses)."
  ]
}
```

---

## ⚖️ SEBI Compliance Notice

> **Disclaimer**: ET AI Money Mentor is an AI-powered tool designed for **educational and informational purposes only**. It does **not** constitute investment advice as defined by the Securities and Exchange Board of India (SEBI). All recommendations generated by this tool are illustrative and based on general financial principles. Users are strongly advised to consult a **SEBI-registered investment advisor** before making any investment decisions. Past performance of any financial instrument is not indicative of future results.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance async REST API framework |
| **LangChain** | Multi-agent orchestration and LLM chaining |
| **Google Gemini 1.5 Pro** | Large Language Model for financial reasoning |
| **Pydantic** | Data validation and serialisation |
| **Uvicorn** | ASGI server for production deployment |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

*Built with ❤️ for the Indian investor.*
