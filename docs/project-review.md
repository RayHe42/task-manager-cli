# Project Review: Task Manager CLI

## 1. Project Overview

Task Manager CLI is a command-line task management tool built with Python. Users add, list, complete, and remove tasks through terminal commands. All data is stored in a local JSON file — no database, no server, no external dependencies.

**Tech stack:** Python 3.10+, argparse, dataclasses, json, pathlib, pytest, Docker, GitHub Actions

**Repository:** [task-manager-cli on GitHub](https://github.com/RayHe42/task-manager-cli)

**Current version:** v0.2.0

## 2. Why I Built This Project

This is a learning project with three specific goals:

1. **Build Python engineering fundamentals** — not just writing scripts, but structuring a real project with packaging, testing, and error handling
2. **Learn Git and GitHub workflows** — feature branches, pull requests, code reviews, semantic versioning, changelogs
3. **Practice AI-assisted development** — learn to collaborate with Claude Code using a "plan first, implement second, test third" workflow

I chose a task manager on purpose. The domain is simple enough that I can focus on engineering practices rather than business logic. Every decision — from data model to Docker setup — is something I had to think through and can explain.

## 3. Core Features

| Command | What it does |
|---------|-------------|
| `task add <title>` | Add a new task with auto-incrementing ID |
| `task list` | List all tasks |
| `task list --todo` | Show only incomplete tasks |
| `task list --done` | Show only completed tasks |
| `task done <id>` | Mark a task as done |
| `task remove <id>` | Delete a task |
| `task clear --yes` | Clear all tasks (requires confirmation) |

**Non-obvious features:**
- Empty or whitespace-only titles are rejected with a clear error message
- `--todo` and `--done` are mutually exclusive (enforced by argparse)
- `task clear` requires `--yes` flag to prevent accidental data loss
- `TASK_MANAGER_DATA_FILE` environment variable overrides the default storage path (used by Docker Compose)

**Test coverage:** 32 tests (8 for storage, 24 for CLI) covering happy paths, edge cases, and error conditions.

## 4. Engineering Highlights

### 4.1 Three-layer architecture

```
cli.py          → Parses commands, dispatches to handlers
storage.py      → Reads/writes JSON, manages IDs
models.py       → Defines Task dataclass
```

Each layer has a single responsibility. `cli.py` knows about argparse and stdout. `storage.py` knows about files and JSON. `models.py` knows about data structure. They don't cross boundaries — `cli.py` never touches JSON directly, `storage.py` never prints to the terminal.

### 4.2 Zero external dependencies

The entire project uses only Python standard library. This was a deliberate constraint: if I can't build it with built-in tools, I don't understand the fundamentals well enough. The only non-standard dependency is pytest (for testing, declared in `[project.optional-dependencies]`).

### 4.3 Test isolation with tmp_path and monkeypatch

Every test runs in its own temporary directory. No test reads or writes to the real `tasks.json`. This means:
- Tests can run in parallel without conflicts
- Tests don't pollute the developer's working directory
- CI doesn't need special setup

The CLI tests use `monkeypatch` to redirect `DEFAULT_TASKS_FILE` to a temp path. The storage tests use pytest's `tmp_path` fixture directly.

### 4.4 Docker Compose with volume persistence

Running tasks inside a container normally means data disappears when the container exits. I solved this with a named Docker volume:

```yaml
services:
  task:
    build: .
    volumes:
      - task-manager-data:/data
    environment:
      - TASK_MANAGER_DATA_FILE=/data/tasks.json
```

The `TASK_MANAGER_DATA_FILE` environment variable tells the app to store data in the volume, so tasks persist across container runs.

### 4.5 CI on every push

GitHub Actions runs `make test` on every push and pull request. This catches regressions immediately. The workflow is minimal — Python 3.11 on Ubuntu, install dependencies, run tests. No complex matrix builds or deployment steps.

### 4.6 Semantic versioning and changelog

The project follows [Keep a Changelog](https://keepachangelog.com/) format and semantic versioning:
- v0.1.0: Core functionality (CLI, storage, tests)
- v0.2.0: Engineering infrastructure (Docker, CI, Makefile, validation, contributing guide)

Each version has a clear scope. The changelog makes it easy to see what changed and when.

## 5. What I Learned

### Python packaging
- How `pyproject.toml` works as the single source of project metadata
- How `[project.scripts]` creates an installable CLI command
- The difference between `pip install .` and `pip install -e .`

### Data modeling with dataclasses
- Using `@dataclass` for clean struct definitions
- Implementing `to_dict()` / `from_dict()` for JSON serialization
- Why `asdict()` is better than manual dictionary conversion

### CLI design with argparse
- Subcommands (`add`, `list`, `done`, `remove`, `clear`)
- Mutually exclusive argument groups (`--todo` vs `--done`)
- Using `sys.exit(1)` for error cases vs `sys.exit(0)` for success

### Testing practices
- `tmp_path` fixture for file system isolation
- `monkeypatch` for redirecting module-level constants
- `capsys` for capturing stdout/stderr in CLI tests
- Testing error cases, not just happy paths

### Docker fundamentals
- Writing a minimal Dockerfile with `python:3.12-slim`
- Using named volumes for data persistence
- Docker Compose for simplifying container commands

### Git and GitHub workflows
- Feature branches and pull requests
- Writing meaningful commit messages
- Semantic versioning (major.minor.patch)
- Maintaining a changelog

### AI-assisted development
- Writing a CLAUDE.md file to define collaboration rules
- "Plan first, implement second, test third" workflow
- How to give clear requirements so Claude Code produces correct output

## 6. Problems I Encountered

### Accidentally committing generated files
Early in the project, I committed `__pycache__/` and `*.egg-info/` directories. I had to remove them from version control and add a proper `.gitignore`. Lesson: set up `.gitignore` before your first commit, not after.

### Docker data disappearing
When I first ran the CLI in Docker, tasks disappeared after each container run. I initially tried bind mounts, but they had permission issues. The solution was Docker named volumes combined with the `TASK_MANAGER_DATA_FILE` environment variable.

### Test interference
Early tests wrote to the real `tasks.json` in the project root. If I had tasks in my local file, tests would fail or produce wrong results. Fixing this required learning about `tmp_path` and `monkeypatch` to isolate test environments.

### Deciding on project structure
I initially put everything in one file. As the project grew, I had to decide how to split into `cli.py`, `storage.py`, and `models.py`. The key insight: each file should have one reason to change. If I change how commands are parsed, only `cli.py` changes. If I change how data is stored, only `storage.py` changes.

## 7. How Claude Code Helped

I used Claude Code as a development partner, not a code generator. The workflow was:

1. **I describe what I want** in plain language (e.g., "add Docker support with persistent data")
2. **Claude Code proposes a plan** — which files to create, what each file should contain, why
3. **I review and approve** the plan before any code is written
4. **Claude Code implements** the approved plan
5. **I verify** by running tests and manually testing the feature

The CLAUDE.md file in the repository defines the collaboration rules:
- Always plan before implementing
- Never auto-commit
- Only use standard library + pytest
- Explain every change after implementation

This workflow taught me how to break down requirements, review technical proposals, and verify output — skills that transfer to any team collaboration.

## 8. What I Can Explain Myself

If asked in an interview, I can explain:

- **Why I chose JSON over SQLite** — the data model is simple (one list of tasks), JSON is human-readable and easy to debug, and the project constraint was "no external dependencies"
- **Why I used argparse over click/typer** — argparse is built-in, which aligns with the zero-dependency constraint. It's also what most Python developers encounter first
- **Why I separated cli.py, storage.py, and models.py** — single responsibility principle. Each module has one job and one reason to change
- **How the test isolation works** — `tmp_path` gives each test its own directory, `monkeypatch` redirects the storage path constant, so no test touches the real file system
- **How Docker Compose volume persistence works** — the named volume mounts to `/data` inside the container, the environment variable tells the app to use `/data/tasks.json`, so data survives container restarts
- **How CI catches regressions** — GitHub Actions runs `make test` on every push, so if a change breaks a test, I know immediately

## 9. What I Would Improve Next

| Improvement | Why |
|-------------|-----|
| Task editing (`task edit <id> "new title"`) | Most requested missing feature |
| Task search (`task search "keyword"`) | Useful when task list grows |
| Task priority levels | Adds depth to the data model |
| Color-coded output | Better terminal UX |
| `task --version` command | Users expect version info from CLI tools |
| Test coverage report | `pytest --cov` to quantify coverage |
| Type checking with mypy | Catch type errors before runtime |

These are all future work. The current scope is intentional — keep it simple, ship it, then iterate.

## 10. Portfolio Summary

**What this project demonstrates:**

- Python project packaging and CLI development
- Clean code architecture with separation of concerns
- Test-driven development with proper isolation
- Docker containerization with data persistence
- CI/CD pipeline with GitHub Actions
- Git workflow with semantic versioning and changelogs
- AI-assisted development with clear collaboration rules
- Ability to document, review, and explain technical decisions

**What this project intentionally avoids:**

- Third-party dependencies (proves I understand the fundamentals)
- Over-engineering (no database, no API, no frontend — the problem doesn't require them)
- Magic (every piece of the system is something I can explain from scratch)

**Project stats:**

- 4 source files, ~175 lines of application code
- 2 test files, 32 tests
- 2 versions released (v0.1.0, v0.2.0)
- 100% standard library (except pytest)
