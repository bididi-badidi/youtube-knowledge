from typing import Protocol

from youtube_knowledge.config import Settings


class Embedder(Protocol):
    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


class SentenceTransformerEmbedder:
    def __init__(self, model_name: str) -> None:
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]


class OpenAIEmbedder:
    def __init__(self, model_name: str, api_key: str | None = None) -> None:
        from openai import OpenAI

        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(model=self.model_name, input=texts)
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]


def build_embedder(settings: Settings) -> Embedder:
    if settings.embedding_provider == "openai":
        return OpenAIEmbedder(settings.openai_embedding_model, settings.openai_api_key)
    return SentenceTransformerEmbedder(settings.local_embedding_model)
