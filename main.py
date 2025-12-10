from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
import yfinance as yf
from dotenv import load_dotenv
from typing import Literal

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser 

load_dotenv()

app = FastAPI(title="Mini Disruptor Scoring Endpoint (LangChain v1 + Tools)")


class TickerRequest(BaseModel):
    ticker: str


class DisruptorScore(BaseModel):
    summary: str
    risk_score: Literal[1, 2, 3, 4, 5]
    opportunity_score: Literal[1, 2, 3, 4, 5]


# LangChain model
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7)


# -----------------------
# Tool 1: Validate ticker
# -----------------------
def validate_ticker(ticker: str) -> bool:
    try:
        tk = yf.Ticker(ticker)
        info = tk.info
        return "longName" in info and info["longName"] != ""
    except Exception:
        return False


# -----------------------
# Tool 2: Get company info
# -----------------------
def get_company_info(ticker: str) -> dict:
    tk = yf.Ticker(ticker)
    info = tk.info
    return {
        "name": info.get("longName", ""),
        "sector": info.get("sector", ""),
        "industry": info.get("industry", ""),
        "marketCap": info.get("marketCap", 0),
        "summary": info.get("longBusinessSummary", "")
    }


# -----------------------
# API Endpoint
# -----------------------
@app.post("/score-company")
async def score_company(request: TickerRequest):
    ticker = request.ticker.upper().strip()

    # Step 1: Validate ticker
    if not ticker.isalpha() or len(ticker) > 5:
        raise HTTPException(status_code=400, detail="Invalid ticker format")
    if not validate_ticker(ticker):
        raise HTTPException(status_code=404, detail="Ticker not found")

    # Step 2: Get company info
    company_info = get_company_info(ticker)

    # Step 3: Build prompt and parser
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a financial analyst and expert in disruptive companies."),
        ("human", "Here is some company info:\n"
                  "Name: {name}\n"
                  "Sector: {sector}\n"
                  "Industry: {industry}\n"
                  "MarketCap: {marketCap}\n"
                  "Summary: {summary}\n\n"
                  "Based on this info, give me a simple 3-sentence summary of why {ticker} might be considered a disruptor. "
                  "Respond in JSON with fields: summary, risk_score (1–5), opportunity_score (1–5).")
    ])

    # Use structured output with Pydantic
    parser = PydanticOutputParser(pydantic_object=DisruptorScore)
    prompt_with_parser = prompt | llm | parser

    try:
        result = prompt_with_parser.invoke({
            "ticker": ticker,
            "name": company_info["name"],
            "sector": company_info["sector"],
            "industry": company_info["industry"],
            "marketCap": company_info["marketCap"],
            "summary": company_info["summary"]
        })

        return {"ticker": ticker, **result.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
