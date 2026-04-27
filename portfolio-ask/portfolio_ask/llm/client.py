import requests
import json
from portfolio_ask.models.response import AnswerResponse

def generate_answer(query, context):
    prompt = f"""
You are a financial assistant.

You are given:
1. Portfolio holdings
2. Relevant context (news or additional data)

Your tasks:

1. If the question asks for:
highest, lowest, best, worst, or comparison
Then:
- Do NOT show step-by-step comparisons
- Find the answer directly using the given values
- Return a short and clear answer

2. If the question asks for calculations (like total exposure):
- Show step-by-step calculation using CURRENT PRICE only
- Do NOT use average cost unless explicitly asked

3. If the question is about news:
- Identify relevant news
- Explain impact clearly and concisely

Important rules (very strict):

- Use ONLY the data provided in the context
- Do NOT assume or infer missing values
- Do NOT make up stock names, prices, or quantities
- If required data is missing, say "Insufficient data"

- Always use the "value" field if available instead of recalculating unnecessarily
- If performing calculations, ensure numbers match the context exactly
- If numeric values are present, return them as numbers, not strings

- Do NOT list all items unless explicitly asked
- Do NOT repeat the entire dataset in the answer
- If sector data is available, use it to analyze diversification
- Do NOT return "Insufficient data" for diversification questions if sectors are present
- If multiple stocks belong to the same sector, treat it as concentration and mention it in diversification analysis
- If you mention a stock in the answer, you MUST include it in the "stock" field.
- No markdown
- No bullet points
- Keep answers clean and concise



Context:
{context}

Question:
{query}

Return the answer strictly in JSON format.

Rules:
- Always include "answer"
- If a stock is identified, "stock" MUST be included
- If a numeric value is used, include it (e.g., "value", "total")

- Do NOT include any field with null or empty values
- Do NOT include unnecessary fields

- The answer must be complete and include key values (e.g., include amount)

Examples:

{{
  "answer": "TCS has the highest investment value of 152000 INR.",
  "stock": "TCS",
  "value": 152000
}}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    raw_text = response.json()["response"].strip()

    try:
        # 🔥 First attempt: direct JSON
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            # 🔥 Fallback: extract JSON block
            import re
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                data = json.loads(match.group())
            else:
                raise

        # 🔥 Validate using Pydantic
        validated = AnswerResponse(**data)

        return validated.dict()

    except Exception:
        return {
            "answer": raw_text
        }