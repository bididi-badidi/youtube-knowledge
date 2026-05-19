import chromadb

from youtube_knowledge.embeddings import Embedder
from youtube_knowledge.models import ChunkRecord


class ChromaVectorStore:
    def __init__(self, path: str, collection_name: str, embedder: Embedder) -> None:
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = embedder

    def add_chunks(self, chunks: list[ChunkRecord]) -> None:
        if not chunks:
            return

        embeddings = self.embedder.embed_documents([chunk.text for chunk in chunks])
        self.collection.upsert(
            ids=[chunk.id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            embeddings=embeddings,
            metadatas=[chunk.metadata for chunk in chunks],
        )

    def query(
        self,
        text: str,
        n_results: int = 5,
        where: dict[str, str] | None = None,
    ) -> dict:
        return self.collection.query(
            query_embeddings=[self.embedder.embed_query(text)],
            n_results=n_results,
            where=where,
        )
