# Task Manager CLI

A simple command-line task manager built with Python. Tasks are stored in a local JSON file — no database, no server, no external dependencies.

## Why This Project

This is a learning project designed to practice Python engineering fundamentals:

- **CLI development** — building a usable command-line tool with `argparse`
- **Data modeling** — structuring data with Python `dataclass`
- **File I/O** — reading and writing JSON with error handling
- **Testing** — writing unit tests with `pytest`
- **Project packaging** — using `pyproject.toml` to create an installable CLI command

## Features

- Add, list, complete, and remove tasks
- Filter tasks by status: `--todo` (incomplete) or `--done` (completed)
- Clear all tasks at once with confirmation
- Input validation — rejects empty or whitespace-only task titles
- Auto-incrementing task IDs
- Data persisted to local `tasks.json`
- Graceful error handling for missing or corrupt data files
- Zero external dependencies — Python standard library only

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Language | Python 3.10+ | Modern type hints (`list[Task]`) |
| CLI parsing | `argparse` | Built-in, no extra dependency |
| Data storage | `json` | Human-readable, easy to debug |
| Data model | `dataclasses` | Clean structure with `asdict()` serialization |
| File paths | `pathlib` | Cross-platform path handling |
| Testing | `pytest` | Simple syntax, powerful fixtures |
| Container | Docker | Reproducible environment, no local Python needed |
| Orchestration | Docker Compose | Simplified container commands with persistent volumes |

## Quick Commands (Make)

If you have `make` installed, common tasks are wrapped in a Makefile:

```bash
make                      # Show all available commands
make install              # Install in dev mode
make test                 # Run all tests
make clean                # Remove __pycache__ and .pytest_cache
make docker-build         # Build Docker image
make compose-build        # Build with Docker Compose
make compose-list         # List tasks (inside Docker)
make compose-add TITLE="Buy groceries"   # Add a task (inside Docker)
make compose-down         # Stop containers (keep data)
make compose-down-volumes # Stop containers and delete all task data
```

## Installation

### With pip (recommended for development)

```bash
git clone https://github.com/<your-username>/task-manager-cli.git
cd task-manager-cli
pip install -e .
```

After installation, the `task` command is available directly in your terminal.

### With Docker

```bash
git clone https://github.com/<your-username>/task-manager-cli.git
cd task-manager-cli
docker build -t task-manager .
docker run --rm task-manager
```

To run tests in Docker:

```bash
docker run --rm task-manager pytest -q
```

To persist tasks across container runs, use a named volume:

```bash
# Add a task (data saved to Docker volume)
docker run --rm -v task-data:/data -e TASK_MANAGER_DATA_FILE=/data/tasks.json task-manager task add "Learn Docker"

# List tasks (data persists between runs)
docker run --rm -v task-data:/data -e TASK_MANAGER_DATA_FILE=/data/tasks.json task-manager task list
```

### With Docker Compose (recommended)

Docker Compose simplifies the commands — no need to remember volume and environment variable flags every time.

```bash
# Add a task
docker compose run --rm task task add "Learn Docker"

# List tasks
docker compose run --rm task task list

# Mark a task as done
docker compose run --rm task task done 1

# Remove a task
docker compose run --rm task task remove 1

# Clear all tasks
docker compose run --rm task task clear --yes

# Run tests
docker compose run --rm task pytest -q
```

The `--rm` flag automatically removes the container after each command. Task data is persisted in a Docker volume (`task-manager-data`), so your tasks survive across runs.

> **Note:** `docker compose down -v` deletes the volume and all task data. Use `docker compose down` (without `-v`) if you just want to stop containers.

## Usage

```bash
# Add tasks
$ task add "Buy groceries"
Added task 1: Buy groceries

$ task add "Write code"
Added task 2: Write code

# Empty titles are rejected
$ task add ""
Error: task title cannot be empty.

$ task add "   "
Error: task title cannot be empty.

# Mark a task as done
$ task done 1
Marked task 1 as done.

# List all tasks
$ task list
  [✓] 1. Buy groceries
  [ ] 2. Write code

# Filter by status
$ task list --todo
  [ ] 2. Write code

$ task list --done
  [✓] 1. Buy groceries

# Remove a task
$ task remove 1
Removed task 1.

# Clear all tasks (requires --yes flag)
$ task clear --yes
All tasks cleared.
```

## Command Reference

| Command | Description |
|---------|-------------|
| `task add <title>` | Add a new task |
| `task list` | List all tasks |
| `task list --todo` | List only incomplete tasks |
| `task list --done` | List only completed tasks |
| `task done <id>` | Mark a task as done |
| `task remove <id>` | Remove a task |
| `task clear --yes` | Clear all tasks (confirmation required) |
| `task --help` | Show help message |

## Running Tests

```bash
# Run all tests
pytest -v

# Run with coverage summary
pytest --tb=short -q

# Run a specific test file
pytest tests/test_storage.py -v
pytest tests/test_cli.py -v
```

The project includes **32 tests** covering:

- `test_storage.py` (8 tests) — load, save, clear, next ID generation, parent directory creation, corrupt JSON handling
- `test_cli.py` (24 tests) — all CLI commands, input validation, environment variable config, status filtering, error cases for nonexistent tasks, combined operations

## CI

Every push and pull request triggers a GitHub Actions workflow that:

1. Sets up Python 3.11 on Ubuntu
2. Installs dependencies from `requirements.txt` and `pyproject.toml`
3. Runs `make test`

You can see the workflow status in the **Actions** tab of the GitHub repository.

## Project Structure

```
task-manager-cli/
├── src/task_manager/
│   ├── __init__.py
│   ├── cli.py          # Entry point — parses CLI args, dispatches to command handlers
│   ├── models.py       # Task dataclass with serialization methods
│   └── storage.py      # JSON file I/O: load, save, clear, ID generation
├── tests/
│   ├── test_cli.py     # CLI integration tests (24 tests)
│   └── test_storage.py # Storage unit tests (8 tests)
├── Dockerfile          # Docker image definition
├── compose.yaml        # Docker Compose configuration
├── Makefile            # Common development commands
├── .dockerignore       # Files excluded from Docker build
├── pyproject.toml      # Package metadata and CLI entry point
├── CLAUDE.md           # AI-assisted development guidelines
└── tasks.json          # Local data file (gitignored)
```

**Data flow:**

```
User types command
    → cli.py (argparse parses arguments)
    → storage.py (loads tasks from tasks.json)
    → command handler (modifies task list)
    → storage.py (saves back to tasks.json)
```

## Engineering Practices

- **No external dependencies** — uses only Python standard library + pytest
- **Type hints** — `list[Task]`, `dict`, return type annotations throughout
- **Dataclass serialization** — clean `to_dict()` / `from_dict()` pattern
- **Error handling** — graceful messages for missing files, corrupt JSON, nonexistent task IDs
- **Test isolation** — each test uses a temporary directory via `tmp_path` fixture
- **Mutually exclusive flags** — `--todo` and `--done` cannot be used together (enforced by argparse)
- **Git workflow** — feature branches, meaningful commit messages
- **CI** — GitHub Actions runs `make test` on every push and pull request

## Roadmap

Planned features for future development:

- [ ] Task editing (`task edit <id> "new title"`)
- [ ] Task search (`task search "keyword"`)
- [ ] Task priority levels
- [ ] Due date support
- [ ] Color-coded terminal output

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, coding standards, and pull request guidelines.

## License

This project is for learning purposes.
