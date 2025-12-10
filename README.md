# Mini Disruptor Scoring Endpoint (LangChain + Tools)

## Overview

This is a small FastAPI demo that scores a company as a **disruptor** using an LLM (LangChain + ChatGroq) and company info from **Yahoo Finance** (`yfinance`).

The API validates the stock ticker, fetches company info, and then generates a short JSON report containing:

* `summary`: 3-sentence disruptor explanation
* `risk_score` (1–5)
* `opportunity_score` (1–5)

---

## Features

1. **Ticker validation** – ensures the ticker exists.
2. **Company info augmentation** – provides the LLM with real company data.
3. **LangChain v1 integration** – generates structured JSON output.
4. **Error handling** – invalid tickers or malformed responses return clear HTTP errors.

---

## Requirements

* Python 3.11+
* Install dependencies using uv (Universal Python Package Manager):

```
uv install -r requirements.txt
```

* Create a `.env` file in the root directory with your Groq API key:

```
GROQ_API_KEY=gsk_...
```

* Get your API key from: [https://groq.com/](https://groq.com/)

---

## Usage

### Run locally

```
uv run uvicorn main:app --reload
```

The API will run at:

```
http://127.0.0.1:8000
```

### Endpoint

`POST /score-company`

**Request Body**

```
{
  "ticker": "TSLA"
}
```

**Example Response**

```
{
  "ticker": "TSLA",
  "summary": "Tesla is revolutionizing the automotive industry with electric vehicles and sustainable energy solutions...",
  "risk_score": 3,
  "opportunity_score": 5
}
```

### Errors

* `400 Bad Request` – ticker format invalid (non-alpha or >5 chars)
* `404 Not Found` – ticker does not exist
* `500 Internal Server Error` – LLM returned invalid JSON or other unexpected errors

---

## Assumptions

* Only US tickers are supported (Yahoo Finance coverage).
* LLM responses are expected in JSON format.
* No database or authentication; intended for local demo/testing.

---

## Improvements (Future)

* Add HTML output option (lightweight snippet).
* Cache ticker/company info to reduce repeated API calls.
* Extend to international tickers or other exchanges.
* Retry mechanism for LLM failures or timeouts.
