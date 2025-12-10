# Mini Disruptor Scoring Endpoint (LangChain + Groq)

Tiny FastAPI demo that uses Groq + LangChain to score how disruptive a company is. Pulls real-time data from Yahoo Finance (`yfinance`) and returns clean JSON.

The API validates the stock ticker, fetches company info, and then generates a short JSON report containing:

* `summary`: 3-sentence disruptor explanation
* `risk_score` (1–5)
* `opportunity_score` (1–5)

---

## Features

* Validates real stock tickers
* Fetches live company data from Yahoo Finance
* Forces the LLM to return valid JSON (using Pydantic output parser)
* Proper error handling (400/404/500 with clear messages)

---

## Requirements

* Python 3.11+
* **uv** (faster than pip/poetry, recommended)

---

## Setup (2025 style)

1. **Install uv** if you don’t have it:

```bash
pip install uv   # or brew install uv, or curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone the repo** and cd into it

3. **Install dependencies**

* With `pyproject.toml` (creates venv + installs all deps including dev):

```bash
uv sync --frozen
```

* With `requirements.txt` only:

```bash
py -m venv .venv
.venv/scripts/activate
pip install -r requirements.txt
```

4. **Configure your .env**

```bash
cp .env.example .env
```

Then edit `.env` and add your Groq key:

```text
GROQ_API_KEY=gsk_your_key_here
```

Get one for free at: [https://console.groq.com/keys](https://console.groq.com/keys)

---

## How to run

```bash
uv run fastapi dev
```
or 

```bash
fastapi dev
```

 
Swagger docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Endpoint

`POST /score-company`

**Request Body**

```json
{
  "ticker": "NVDA"
}
```

**Example Response**

```json
{
  "ticker": "NVDA",
  "summary": "NVIDIA basically prints money with AI chips and has a near monopoly on training hardware...",
  "risk_score": 2,
  "opportunity_score": 5
}
```

---

## Error Responses

* `400` → invalid ticker (numbers, too long, garbage)
* `404` → ticker doesn’t exist on Yahoo Finance
* `500` → LLM returned invalid JSON (rare with Groq + output parser)
