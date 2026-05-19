from youtube_knowledge.config import Settings


class TranscriptSummarizer:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def summarize(self, title: str, transcript_text: str, max_chars: int = 900) -> str:
        if self.settings.gemini_api_key:
            return self._summarize_with_gemini(title, transcript_text, max_chars)
        return self._extractive_summary(title, transcript_text, max_chars)

    def _summarize_with_gemini(
        self,
        title: str,
        transcript_text: str,
        max_chars: int,
    ) -> str:
        from google import genai

        client = genai.Client(api_key=self.settings.gemini_api_key)
        response = client.models.generate_content(
            model=self.settings.gemini_model,
            contents=(
                "Summarize this YouTube transcript for a Telegram group. "
                "Keep it concise, concrete, and useful.\n\n"
                f"Title: {title}\n\nTranscript:\n{transcript_text[:12000]}"
            ),
        )
        return response.text[:max_chars]

    def _extractive_summary(
        self, title: str, transcript_text: str, max_chars: int
    ) -> str:
        cleaned = " ".join(transcript_text.split())
        summary = cleaned[:max_chars].strip()
        suffix = "..." if len(cleaned) > max_chars else ""
        return f"{title}\n\n{summary}{suffix}"
