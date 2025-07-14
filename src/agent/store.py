from langgraph.store.memory import InMemoryStore, IndexConfig
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def get_store_with_embeddings(google_embeddings_model: str, fields: list[str] | None = None) -> InMemoryStore:
    embeddings_model = GoogleGenerativeAIEmbeddings(model=google_embeddings_model)
    memory_store = InMemoryStore(
        index=IndexConfig(
            embed=embeddings_model,
            dims=1024,
            fields=fields or ["$"]
        )
    )
    return memory_store
