import argparse

from youtube_knowledge.config import Settings
from youtube_knowledge.models import VideoMetadata


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest YouTube transcripts into a vector database.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest-video", help="Ingest one YouTube video")
    ingest.add_argument("--video-id", required=True)
    ingest.add_argument("--title", required=True)
    ingest.add_argument("--channel", required=True)
    ingest.add_argument("--genre", required=True)
    ingest.add_argument("--published-at")
    ingest.add_argument("--source-url")
    ingest.add_argument("--no-notify", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "ingest-video":
        from youtube_knowledge.pipeline import YouTubeIngestionPipeline

        source_url = args.source_url or f"https://youtube.com/watch?v={args.video_id}"
        video = VideoMetadata(
            video_id=args.video_id,
            video_title=args.title,
            channel_name=args.channel,
            genre=args.genre,
            published_at=args.published_at,
            source_url=source_url,
        )
        result = YouTubeIngestionPipeline(Settings()).ingest_video(
            video,
            notify=not args.no_notify,
        )
        print(f"Stored {result.chunks_stored} chunks for {result.video_id}")
