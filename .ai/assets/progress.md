# Project Progress

## Current Task

- [ ] Implement planned runtime surfaces from the README:
  WebSub/FastAPI webhook ingestion, APScheduler fallback polling, Docker
  packaging, and a RAG query interface.

## Upcoming

- [ ] Improve chunk timestamp attribution so source URLs are based on segment
  boundaries rather than substring matching.
- [ ] Add stale chunk handling for re-ingestion, using `chunk_version` metadata
  as part of the cleanup/query strategy.

## Project Documents

- [Project Description](../../README.md)
- [Architecture & Plan](.ai/assets/PLAN.md)
- [Session Notes](.ai/assets/session_notes.md)
- [Backlog](.ai/assets/backlog.md)
- [Task Archive](.ai/assets/task_archive.md)

## Phases

- [x] Project description and tech stack documented: [README](../../README.md)
- [x] UV-managed ingestion environment and pipeline scaffold complete:
  [README](../../README.md)
- [ ] Runtime ingestion automation and query surfaces:
  [README](../../README.md)
