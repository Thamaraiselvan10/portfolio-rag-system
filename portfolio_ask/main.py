from portfolio_ask.data_pipeline.loader import load_all_documents
from portfolio_ask.data_pipeline.chunker import chunk_documents
from portfolio_ask.retrieval.embedder import embed_texts
from portfolio_ask.retrieval.vector_store import VectorStore
from portfolio_ask.retrieval.retriever import Retriever
from portfolio_ask.llm.client import generate_answer
from portfolio_ask.validator.validator import validate_answer
from portfolio_ask.utils.helpers import extract_tickers, filter_news_by_portfolio
from portfolio_ask.utils.helpers import clean_text
from portfolio_ask.utils.helpers import compute_portfolio_metrics
from portfolio_ask.utils.helpers import detect_query_type


def remove_nulls(data):
    if isinstance(data, dict):
        return {k: remove_nulls(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [remove_nulls(v) for v in data]
    else:
        return data

def run(query: str):
    """
    Main pipeline:
    Query → Retrieve → Smart Routing → LLM → Validate → Output
    """

    # 1. Load data
    docs = load_all_documents()

    # 2. Chunk
    chunked_docs = chunk_documents(docs)

    # 3. Embed
    texts = [doc["text"] for doc in chunked_docs]
    embeddings = embed_texts(texts)

    # 4. Vector store
    store = VectorStore(dimension=len(embeddings[0]))
    store.add(embeddings, chunked_docs)

    # 5. Retriever
    retriever = Retriever(store)
    results = retriever.retrieve(query)

    # 6. Extract portfolio info
    portfolio_docs = [d for d in chunked_docs if d["type"] == "portfolio"]
    tickers = extract_tickers(portfolio_docs)

    # 7. Smart routing (UPDATED)

    intent = detect_query_type(query)

    # 🔥 Portfolio queries
    if intent == "portfolio":
        stocks = compute_portfolio_metrics(portfolio_docs)

        context = f"""
Portfolio Data:
{stocks}
"""
        used_results = portfolio_docs

    # 🔥 News queries
    elif intent == "news":
        filtered_news = filter_news_by_portfolio(chunked_docs, tickers)

        portfolio_context = "\n\n".join([p["text"] for p in portfolio_docs])
        news_context = "\n\n".join([n["text"] for n in filtered_news[:5]])

        context = f"""
Portfolio:
{portfolio_context}

Relevant News:
{news_context}
"""
        used_results = filtered_news[:5]

    # 🔥 Default (retriever)
    else:
        context = "\n\n".join([r["text"] for r in results])
        used_results = results

    # 8. Generate answer
    response = generate_answer(query, context)

# 🔥 CLEAN NULL FIELDS HERE
    response = remove_nulls(response)

    answer = clean_text(response.get("answer", ""))

    # 9. Validate
    # 🔥 use enriched data instead of raw text
    validation_context = context   # this includes computed values

    validation = validate_answer(answer, [{"text": validation_context}])

    # 10. Output
    output = {
        "query": query,
        "answer": answer,
        "structured": response,   # 🔥 important
        "sources": list(set([r["source"] for r in used_results])),
        "validation": validation
    }

    return output


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py \"your query\"")
    else:
        result = run(sys.argv[1])
        print(result)