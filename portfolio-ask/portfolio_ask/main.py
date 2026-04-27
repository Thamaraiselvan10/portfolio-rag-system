from portfolio_ask.data_pipeline.loader import load_all_documents
from portfolio_ask.data_pipeline.chunker import chunk_documents
from portfolio_ask.retrieval.embedder import embed_texts
from portfolio_ask.retrieval.vector_store import VectorStore
from portfolio_ask.retrieval.retriever import Retriever
from portfolio_ask.llm.client import generate_answer
from portfolio_ask.validator.validator import validate_answer


def run(query: str):
    """
    Main pipeline:
    Query → Retrieve → LLM → Validate → Output
    """

    # 1. Load data
    docs = load_all_documents()

    # 2. Chunk
    chunked_docs = chunk_documents(docs)

    # 3. Embed
    texts = [doc["text"] for doc in chunked_docs]
    embeddings = embed_texts(texts)

    # 4. Create vector store
    store = VectorStore(dimension=len(embeddings[0]))
    store.add(embeddings, chunked_docs)

    # 5. Retrieve relevant chunks
    retriever = Retriever(store)
    results = retriever.retrieve(query)

    # 6. Build context
    context = "\n\n".join([r["text"] for r in results])

    # 7. Generate answer
    answer = generate_answer(query, context)

    # 8. Validate answer
    validation = validate_answer(answer, results)

    # 9. Prepare structured output
    output = {
        "query": query,
        "answer": answer,
        "sources": list(set([r["source"] for r in results])),
        "validation": validation
    }

    return output


# Optional: allow direct run (not required for -m, but useful)
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py \"your query\"")
    else:
        result = run(sys.argv[1])
        print(result)