from portfolio_ask.retrieval.embedder import embed_texts

class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query, top_k=3):
        query_embedding = embed_texts([query])[0]
        results = self.vector_store.search(query_embedding, top_k)
        return results