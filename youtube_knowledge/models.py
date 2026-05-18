from pydantic import BaseModel, Field, HttpUrl


class TranscriptSegment(BaseModel):
    text: str
    start: float
    duration: float = 0.0


class VideoMetadata(BaseModel):
    video_id: str
    video_title: str
    channel_name: str
    genre: str
    published_at: str | None = None
    source_url: HttpUrl | str


class ChunkRecord(BaseModel):
    id: str
    text: str
    metadata: dict[str, str | int | float | None] = Field(default_factory=dict)
