from youtube_knowledge.config import Settings
from youtube_knowledge.summarizer import TranscriptSummarizer


def test_summarizer_uses_local_extractive_fallback_without_openai_key() -> None:
    settings = Settings(openai_api_key=None)
    summary = TranscriptSummarizer(settings).summarize(
        "Video title",
        "One. Two. Three.",
        max_chars=20,
    )

    assert summary.startswith("Video title")
    assert "One. Two. Three." in summary
