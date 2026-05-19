---
name: worktree-bootstrap
description: "Use this skill when creating or preparing git worktrees for this Python repository, especially when the user wants to automate git worktree add, copying .env files, and installing dependencies with uv. Triggers: worktree, git worktree, bootstrap worktree, copy env files, install dependencies in a worktree. Do NOT use for ordinary branch creation without a worktree."
---

# Worktree Bootstrap

Use the repository script instead of manually chaining commands.

## Commands

- Create a new worktree, copy `.env*` files from the current repo, and install dependencies:
  `uv run python scripts/worktree.py add <path> <branch>`
- Create a worktree from a specific base ref:
  `uv run python scripts/worktree.py add <path> <branch> --base <ref>`
- Add an already-existing local branch as a worktree:
  `uv run python scripts/worktree.py add <path> <existing-branch>`
- Bootstrap an existing worktree:
  `uv run python scripts/worktree.py setup <path>`
- Skip dependency install:
  `uv run python scripts/worktree.py add <path> <branch> --no-install`
- Recreate the virtual environment during setup:
  `uv run python scripts/worktree.py setup <path> --reinstall`

## Rules

- Keep `.env*` files uncommitted.
- Prefer sibling worktree paths under `/Users/user/Projects/youtube-knowledge/`, matching the user's existing layout.
- Use `--base` only when creating a new branch; existing branches are attached directly.
- Use `uv sync` through the script for dependency installation instead of calling package installers directly.
- Do not delete existing worktrees unless the user explicitly asks.
