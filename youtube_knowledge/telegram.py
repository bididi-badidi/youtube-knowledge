import asyncio

from telegram import Bot

from youtube_knowledge.config import Settings


class TelegramNotifier:
    def __init__(self, settings: Settings) -> None:
        if not settings.telegram_bot_token or not settings.telegram_chat_id:
            raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required")
        self.bot = Bot(token=settings.telegram_bot_token)
        self.chat_id = settings.telegram_chat_id

    async def send_summary_async(
        self, title: str, summary: str, source_url: str
    ) -> None:
        message = f"*{title}*\n\n{summary}\n\n{source_url}"
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            disable_web_page_preview=False,
        )

    def send_summary(self, title: str, summary: str, source_url: str) -> None:
        asyncio.run(self.send_summary_async(title, summary, source_url))
