from youtube_transcript_api import YouTubeTranscriptApi

from youtube_knowledge.models import TranscriptSegment


class TranscriptFetcher:
    """Fetch transcripts from YouTube without consuming Data API quota."""

    def fetch(
        self, video_id: str, languages: list[str] | None = None
    ) -> list[TranscriptSegment]:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=languages or ["en"],
        )
        return [TranscriptSegment(**segment) for segment in transcript]
