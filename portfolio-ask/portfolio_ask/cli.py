import sys
from portfolio_ask.retrieval.retriever import build_store, retrieve
from portfolio_ask.llm.client import generate_answer
from portfolio_ask.validator.validator import validate


def run(query: str):
    store = build_store()
    chunks = retrieve(query, store)

    context = "\n\n".join([c["text"] for c in chunks])

    answer = generate_answer(query, context)

    validation = validate(answer, chunks)

    sources = list(set([c["source"] for c in chunks]))

    result = {
        "answer": answer,
        "status": validation["status"],
        "reason": validation.get("reason"),
        "sources": sources
    }

    print(result)


if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    run(query)