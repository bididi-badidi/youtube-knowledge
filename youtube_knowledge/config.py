from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    google_api_key: str | None = None
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    webhook_callback_url: str | None = None

    embedding_provider: str = Field(default="local", pattern="^(local|openai)$")
    local_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    openai_embedding_model: str = "text-embedding-3-large"
    gemini_model: str = "gemini-2.5-flash"

    chroma_path: Path = Path(".chroma")
    chroma_collection: str = "youtube_rag"
    chunk_version: str = "v1"

    chunk_size: int = 500
    chunk_overlap: int = 50

    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
