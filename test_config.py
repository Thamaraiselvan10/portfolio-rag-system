from portfolio_ask.data_pipeline.loader import load_all_documents
from portfolio_ask.data_pipeline.chunker import chunk_documents
from portfolio_ask.retrieval.embedder import embed_texts
from portfolio_ask.retrieval.vector_store import VectorStore
from portfolio_ask.retrieval.retriever import Retriever
from portfolio_ask.llm.client import generate_answer
from portfolio_ask.validator.validator import validate_answer

docs = load_all_documents()
chunked = chunk_documents(docs)

texts = [doc["text"] for doc in chunked]
embeddings = embed_texts(texts)

store = VectorStore(dimension=len(embeddings[0]))
store.add(embeddings, chunked)

retriever = Retriever(store)

query = "What is my IT exposure?"

results = retriever.retrieve(query)

# Combine context
context = "\n\n".join([r["text"] for r in results])

answer = generate_answer(query, context)

print("\nAnswer:")
print(answer)

print("\nSources:")
for r in results:
    print(r["source"])

validation = validate_answer(answer, results)

print("\nValidation:")
print(validation)