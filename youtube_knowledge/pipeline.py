from dataclasses import dataclass

from youtube_knowledge.chunking import TranscriptChunker, render_transcript
from youtube_knowledge.config import Settings
from youtube_knowledge.embeddings import build_embedder
from youtube_knowledge.models import VideoMetadata
from youtube_knowledge.summarizer import TranscriptSummarizer
from youtube_knowledge.telegram import TelegramNotifier
from youtube_knowledge.transcripts import TranscriptFetcher
from youtube_knowledge.vector_store import ChromaVectorStore


@dataclass(frozen=True)
class IngestionResult:
    video_id: str
    chunks_stored: int
    summary: str


class YouTubeIngestionPipeline:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.fetcher = TranscriptFetcher()
        self.chunker = TranscriptChunker(
            settings.chunk_size,
            settings.chunk_overlap,
            settings.chunk_version,
        )
        self.summarizer = TranscriptSummarizer(settings)
        self.vector_store = ChromaVectorStore(
            str(settings.chroma_path),
            settings.chroma_collection,
            build_embedder(settings),
        )

    def ingest_video(
        self, video: VideoMetadata, notify: bool = True
    ) -> IngestionResult:
        segments = self.fetcher.fetch(video.video_id)
        chunks = self.chunker.chunk(segments, video)
        self.vector_store.add_chunks(chunks)

        summary = self.summarizer.summarize(
            video.video_title,
            render_transcript(segments),
        )

        if (
            notify
            and self.settings.telegram_bot_token
            and self.settings.telegram_chat_id
        ):
            TelegramNotifier(self.settings).send_summary(
                video.video_title,
                summary,
                str(video.source_url),
            )

        return IngestionResult(
            video_id=video.video_id,
            chunks_stored=len(chunks),
            summary=summary,
        )
