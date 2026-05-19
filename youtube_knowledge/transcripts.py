from youtube_transcript_api import YouTubeTranscriptApi

from youtube_knowledge.models import TranscriptSegment


class TranscriptFetcher:
    """Fetch transcripts from YouTube without consuming Data API quota."""

    def __init__(self) -> None:
        self.client = YouTubeTranscriptApi()

    def fetch(
        self, video_id: str, languages: list[str] | None = None
    ) -> list[TranscriptSegment]:
        transcript = self.client.fetch(
            video_id,
            languages=languages or ["en"],
        )
        return [
            TranscriptSegment(text=item.text, start=item.start, duration=item.duration)
            for item in transcript
        ]
