from dataclasses import dataclass

from youtube_knowledge.transcripts import TranscriptFetcher


@dataclass(frozen=True)
class FakeSnippet:
    text: str
    start: float
    duration: float


class FakeTranscriptClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, list[str]]] = []

    def fetch(self, video_id: str, languages: list[str]) -> list[FakeSnippet]:
        self.calls.append((video_id, languages))
        return [FakeSnippet(text="Hello", start=1.5, duration=2.0)]


def test_transcript_fetcher_uses_current_fetch_api() -> None:
    fetcher = TranscriptFetcher()
    fake_client = FakeTranscriptClient()
    fetcher.client = fake_client

    segments = fetcher.fetch("abc123", languages=["en", "es"])

    assert fake_client.calls == [("abc123", ["en", "es"])]
    assert segments[0].text == "Hello"
    assert segments[0].start == 1.5
    assert segments[0].duration == 2.0
