# YouTube RAG Knowledge Base

A pipeline that watches YouTube channels, transcribes new videos, chunks and tags
the content, then stores it in a vector database for retrieval-augmented
generation (RAG).

## Tech Stack

### 1. Ingestion Layer

| Tool | Purpose | Notes |
|------|---------|-------|
| **YouTube Data API v3** | Fetch video metadata and captions | Requires Google Cloud API key |
| **WebSub / PubSubHubbub** | Webhook trigger on new uploads | Register callback URL per channel |
| **youtube-transcript-api** | Extract auto-generated transcripts | Unofficial but reliable; no quota cost |

```bash
pip install youtube-transcript-api google-api-python-client
```

### 2. Chunking & Processing

| Tool | Purpose | Notes |
|------|---------|-------|
| **LangChain** | Text splitting and RAG pipeline orchestration | Use `RecursiveCharacterTextSplitter` |
| **Python** | Glue logic and metadata construction | 3.10+ recommended |

Chunking strategy:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
```

Metadata schema per chunk:

```json
{
  "channel_name": "Fireship",
  "genre": "tech",
  "video_id": "abc123",
  "video_title": "Every JavaScript Framework Ever",
  "published_at": "2024-11-01T10:00:00Z",
  "chunk_index": 3,
  "timestamp_start": 120.4,
  "source_url": "https://youtube.com/watch?v=abc123&t=120"
}
```

### 3. Embedding

| Tool | Purpose | Notes |
|------|---------|-------|
| **sentence-transformers** | Local, free embedding model | `all-MiniLM-L6-v2` is fast and lightweight |
| **OpenAI Embeddings** | Higher quality, cloud-based embeddings | `text-embedding-3-small`; costs apply |

```bash
pip install sentence-transformers
pip install openai
```

Use `sentence-transformers` for local/free development. Switch to OpenAI for
production if retrieval quality needs to improve.

### 4. Vector Database

| Tool | Purpose | Notes |
|------|---------|-------|
| **ChromaDB** | Store vectors and metadata, filter queries | Recommended fit for channel/genre filtering |
| **FAISS** | Alternative vector index | Faster at large scale, but requires manual metadata handling |

```bash
pip install chromadb
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
| **OpenAI GPT / Claude API** | Generate answers from retrieved chunks | Swap via LangChain's LLM interface |

### 6. Orchestration & Scheduler

| Tool | Purpose | Notes |
|------|---------|-------|
| **FastAPI** | Expose webhook endpoint for WebSub | Lightweight and async-friendly |
| **APScheduler** | Fallback polling if WebSub is unreliable | Poll every 15 minutes as a safety net |
| **Docker** | Containerize the whole pipeline | Keep environments consistent |

```bash
pip install fastapi uvicorn apscheduler
```

## Dependencies

```txt
google-api-python-client
youtube-transcript-api
langchain
langchain-community
sentence-transformers
chromadb
openai
fastapi
uvicorn
apscheduler
python-dotenv
```

## Environment Variables

```env
GOOGLE_API_KEY=your_youtube_data_api_key
OPENAI_API_KEY=your_openai_key
WEBHOOK_CALLBACK_URL=https://your-server.com/webhook
```

`OPENAI_API_KEY` is optional when using local `sentence-transformers`
embeddings.

## Architecture Summary

```text
YouTube Channel
    |
    v (WebSub webhook)
FastAPI Webhook Endpoint
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
RAG Query Interface (LangChain + LLM)
```
