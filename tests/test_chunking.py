from youtube_knowledge.chunking import TranscriptChunker
from youtube_knowledge.models import TranscriptSegment, VideoMetadata


def test_chunker_adds_video_metadata_and_stable_ids() -> None:
    segments = [
        TranscriptSegment(text="First useful sentence about Python.", start=0.0),
        TranscriptSegment(
            text="Second useful sentence about vector search.", start=12.5
        ),
    ]
    video = VideoMetadata(
        video_id="abc123",
        video_title="A useful video",
        channel_name="Test Channel",
        genre="tech",
        published_at="2026-05-18T10:00:00Z",
        source_url="https://youtube.com/watch?v=abc123",
    )

    chunks = TranscriptChunker(chunk_size=120, chunk_overlap=10).chunk(segments, video)

    assert chunks
    assert chunks[0].id == "abc123:0"
    assert chunks[0].metadata["channel_name"] == "Test Channel"
    assert chunks[0].metadata["genre"] == "tech"
    assert chunks[0].metadata["video_id"] == "abc123"
    assert chunks[0].metadata["chunk_index"] == 0
    assert chunks[0].metadata["chunk_version"] == "v1"
    assert chunks[0].metadata["source_url"].startswith("https://youtube.com/watch")
