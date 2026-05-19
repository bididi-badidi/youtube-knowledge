# YouTube RAG Knowledge Base

A Python CLI scaffold for ingesting YouTube transcripts, chunking and tagging
the content, then storing it in ChromaDB for retrieval-augmented generation
(RAG). Channel watching, webhooks, scheduled polling, and the query API are
planned features tracked in project progress.

## Tech Stack

### 1. Ingestion Layer

| Tool | Purpose | Notes |
|------|---------|-------|
| **YouTube Data API v3** | Planned video metadata lookup | Requires Google Cloud API key |
| **WebSub / PubSubHubbub** | Planned webhook trigger on new uploads | Register callback URL per channel |
| **youtube-transcript-api** | Extract auto-generated transcripts | Unofficial but reliable; no quota cost |

```bash
uv add youtube-transcript-api google-api-python-client
```

### 2. Chunking & Processing

| Tool | Purpose | Notes |
|------|---------|-------|
| **LangChain** | Text splitting and RAG pipeline orchestration | Use `RecursiveCharacterTextSplitter` |
| **Python** | Glue logic and metadata construction | 3.10+ recommended |

Current chunking strategy:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
```

The pipeline renders transcript segments as timestamp-prefixed lines, splits the
rendered text into 500-character chunks with 50 characters of overlap, then tags
each chunk with video metadata, a stable `video_id:index` id, and
`chunk_version` metadata. The first matching transcript segment is used to build
the timestamped source URL.

Metadata schema per chunk:

```json
{
  "channel_name": "Fireship",
  "genre": "tech",
  "video_id": "abc123",
  "video_title": "Every JavaScript Framework Ever",
  "published_at": "2024-11-01T10:00:00Z",
  "chunk_index": 3,
  "chunk_version": "v1",
  "timestamp_start": 120.4,
  "source_url": "https://youtube.com/watch?v=abc123&t=120"
}
```

### 3. Embedding

| Tool | Purpose | Notes |
|------|---------|-------|
| **sentence-transformers** | Local, free embedding model | `all-MiniLM-L6-v2` is fast and lightweight |
| **OpenAI Embeddings** | Higher quality, cloud-based embeddings | `text-embedding-3-large`; costs apply |

```bash
uv add sentence-transformers
uv add openai
```

Use `sentence-transformers` for local/free development. Switch to OpenAI
embeddings for production if retrieval quality needs to improve.

### 4. Vector Database

| Tool | Purpose | Notes |
|------|---------|-------|
| **ChromaDB** | Store vectors and metadata, filter queries | Recommended fit for channel/genre filtering |
| **FAISS** | Alternative vector index | Faster at large scale, but requires manual metadata handling |

```bash
uv add chromadb
```

ChromaDB example:

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("youtube_rag")

collection.add(
    documents=["chunk text here..."],
    embeddings=[[0.1, 0.2, 0.3]],
    metadatas=[{"channel_name": "Fireship", "genre": "tech"}],
    ids=["chunk_001"],
)

results = collection.query(
    query_embeddings=[query_vector],
    where={"genre": "tech"},
    n_results=5,
)
```

### 5. RAG & Query Layer

| Tool | Purpose | Notes |
|------|---------|-------|
| **LangChain** | Chain retriever and LLM together | Use `RetrievalQA` or `ConversationalRetrievalChain` |
| **Gemini API** | Generate answers from retrieved chunks | Default generation model: `gemini-2.5-flash` |

### 6. Orchestration & Scheduler

| Tool | Purpose | Notes |
|------|---------|-------|
| **FastAPI** | Planned webhook endpoint for WebSub | Lightweight and async-friendly |
| **APScheduler** | Planned fallback polling | Poll every 15 minutes as a safety net |
| **Docker** | Planned container packaging | Keep environments consistent |

```bash
uv add fastapi uvicorn apscheduler
```

## Dependencies

This project uses `uv` for Python environment and dependency management.

```bash
uv sync
```

```txt
google-api-python-client
youtube-transcript-api
langchain
langchain-community
sentence-transformers
chromadb
google-genai
openai
fastapi
uvicorn
apscheduler
python-dotenv
python-telegram-bot
```

## Environment Variables

```env
GOOGLE_API_KEY=your_youtube_data_api_key
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
WEBHOOK_CALLBACK_URL=https://your-server.com/webhook
TELEGRAM_BOT_TOKEN=123456:replace_me
TELEGRAM_CHAT_ID=-1001234567890
```

`OPENAI_API_KEY` is optional when using local `sentence-transformers`
embeddings. `GEMINI_API_KEY` is optional when using extractive fallback
summaries.

## Usage

Copy `.env.example` to `.env`, fill in the credentials you need, then run the
pipeline through `uv`:

```bash
uv run youtube-knowledge ingest-video \
  --video-id abc123 \
  --title "Every JavaScript Framework Ever" \
  --channel Fireship \
  --genre tech
```

The ingestion pipeline fetches the transcript, chunks it with metadata including
`chunk_version`, embeds the chunks, stores them in ChromaDB, summarizes the
transcript with Gemini when `GEMINI_API_KEY` is set, and sends the summary to
Telegram when `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set.

## Architecture Summary

```text
Manual CLI
    |
    v
Fetch Transcript (youtube-transcript-api)
    |
    v
Chunk + Tag Metadata (LangChain)
    |
    v
Embed (sentence-transformers / OpenAI)
    |
    v
ChromaDB Vector Store
    |
    v
Future RAG Query Interface (Gemini)
```
