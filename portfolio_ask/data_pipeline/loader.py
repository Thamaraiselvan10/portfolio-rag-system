import json
from portfolio_ask.config import PORTFOLIO_PATH #seperate import to avoid circular dependency


def load_portfolio():
    with open(PORTFOLIO_PATH, "r") as f:
        data = json.load(f)

    documents = []

    for item in data:
        text = (
            f"{item['ticker']} is in {item['sector']} sector. "
            f"Quantity: {item['quantity']}. "
            f"Average cost: {item['avg_cost']}. "
            f"Current price: {item['current_price']} {item['currency']}."
        )

        documents.append({
            "text": text,
            "source": "portfolio.json",
            "type": "portfolio"
        })

    return documents

from portfolio_ask.config import NEWS_DIR  #seperate import to avoid circular dependency

def load_news():
    documents = []

    for file in NEWS_DIR.glob("*.md"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "text": text,
            "source": file.name,
            "type": "news"
        })

    return documents


from portfolio_ask.config import GLOSSARY_PATH #seperate import to avoid circular dependency

def load_glossary():
    with open(GLOSSARY_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    return [{
        "text": text,
        "source": "glossary.md",
        "type": "glossary"
    }]

# here, our entire data layer becomes unified and we can easily load all documents for embedding and indexing.

def load_all_documents():
    documents = []

    documents.extend(load_portfolio())
    documents.extend(load_news())
    documents.extend(load_glossary())

    return documents