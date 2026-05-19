from langchain_text_splitters import RecursiveCharacterTextSplitter

from youtube_knowledge.models import ChunkRecord, TranscriptSegment, VideoMetadata


def render_transcript(segments: list[TranscriptSegment]) -> str:
    return "\n".join(f"[{segment.start:.1f}] {segment.text}" for segment in segments)


def find_chunk_start_time(
    chunk_text: str, segments: list[TranscriptSegment]
) -> float | None:
    for segment in segments:
        if segment.text and segment.text[:40] in chunk_text:
            return segment.start
    return segments[0].start if segments else None


class TranscriptChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        chunk_version: str = "v1",
    ) -> None:
        self.chunk_version = chunk_version
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk(
        self,
        segments: list[TranscriptSegment],
        video: VideoMetadata,
    ) -> list[ChunkRecord]:
        chunks = self.splitter.split_text(render_transcript(segments))
        records: list[ChunkRecord] = []

        for index, text in enumerate(chunks):
            timestamp_start = find_chunk_start_time(text, segments)
            source_url = str(video.source_url)
            if timestamp_start is not None:
                source_url = f"https://youtube.com/watch?v={video.video_id}&t={int(timestamp_start)}"

            metadata = {
                "channel_name": video.channel_name,
                "genre": video.genre,
                "video_id": video.video_id,
                "video_title": video.video_title,
                "published_at": video.published_at,
                "chunk_index": index,
                "chunk_version": self.chunk_version,
                "timestamp_start": timestamp_start,
                "source_url": source_url,
            }

            records.append(
                ChunkRecord(
                    id=f"{video.video_id}:{index}",
                    text=text,
                    metadata={
                        key: value
                        for key, value in metadata.items()
                        if value is not None
                    },
                )
            )

        return records
