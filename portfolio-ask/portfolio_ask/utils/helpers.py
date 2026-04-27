def extract_tickers(portfolio_docs):
    """
    Extract stock tickers from portfolio documents
    """
    tickers = []

    for doc in portfolio_docs:
        # Example text: "TCS is in IT sector..."
        ticker = doc["text"].split()[0]
        tickers.append(ticker.upper())

    return tickers


def filter_news_by_portfolio(all_chunks, tickers):
    """
    Filter only those news items that mention portfolio tickers
    """
    relevant_news = []

    for doc in all_chunks:
        if doc["type"] == "news":
            text_lower = doc["text"].lower()

            for ticker in tickers:
                if ticker.lower() in text_lower:
                    relevant_news.append(doc)
                    break  # avoid duplicates

    return relevant_news

import re

def clean_text(text):
    import re

    # Remove markdown bold/italic
    text = re.sub(r'\*\*', '', text)

    # Remove bullet points at line start
    text = re.sub(r'^\s*[\*\-]\s+', '', text, flags=re.MULTILINE)

    # Remove any remaining standalone *
    text = text.replace("*", "")

    # Remove extra spaces
    text = re.sub(r'\n{2,}', '\n', text)

    return text.strip()

# 🔥 Add this at top (below imports)

SECTOR_MAP = {
    "TCS": "IT",
    "INFY": "IT",
    "HDFCBANK": "Banking",
    "ICICIBANK": "Banking",
    "RELIANCE": "Energy",
    "LT": "Infrastructure",
    "SUNPHARMA": "Pharma",
    "TATAMOTORS": "Automobile",
    "HINDUNILVR": "FMCG",
    "BAJFINANCE": "Finance",
    "NIFTYBEES": "ETF",
    "AXISBLUECHIP": "Mutual Fund",
    "SBI_BOND": "Debt",
    "ZOMATO": "Consumer Tech",
    "ADANIENT": "Conglomerate"
}

def compute_portfolio_metrics(portfolio_docs):
    """
    Convert portfolio text into structured data with computed values
    """
    import re

    stocks = []

    for p in portfolio_docs:
        text = p["text"]

        name = re.match(r'([A-Z_]+)', text).group(1)
        sector = SECTOR_MAP.get(name, "Unknown")

        qty = int(re.search(r'Quantity:\s*(\d+)', text).group(1))
        price = int(re.search(r'Current price:\s*(\d+)', text).group(1))

        value = qty * price

        stocks.append({
        "stock": name,
        "quantity": qty,
        "price": price,
        "value": value,
        "sector": sector
    })

    return stocks

def detect_query_type(query: str):
    q = query.lower()

    if any(w in q for w in ["news", "impact", "affect"]):
        return "news"

    if any(w in q for w in ["highest", "lowest", "best", "worst", "compare"]):
        return "portfolio"

    if any(w in q for w in ["total", "exposure", "sum"]):
        return "portfolio"

    if any(w in q for w in ["loss", "profit", "gain", "underperform", "losing"]):
        return "portfolio"
    
    if any(w in q for w in ["diversified", "diversification", "sector"]):
        return "portfolio"

    # 🔥 fallback
    return classify_query_llm(query) # important

import requests

def classify_query_llm(query: str):
    prompt = f"""
Classify this query into one word:
portfolio, news, or general

Query: {query}

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip().lower()