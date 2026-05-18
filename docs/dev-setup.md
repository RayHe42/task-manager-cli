# Developer Setup Guide

This guide walks you through setting up the Task Manager CLI project for local development. It assumes no prior experience with Python project setup.

## What This Project Is

Task Manager CLI is a command-line task manager built with Python. You type commands in the terminal, and the program saves your tasks to a local JSON file. No database, no server — just Python and a file.

```bash
$ task add "Learn Python"
Added task 1: Learn Python

$ task list
  [ ] 1. Learn Python
```

## Prerequisites

Before you start, make sure you have these installed:

| Tool | Minimum Version | Check Command | How to Install |
|------|-----------------|---------------|----------------|
| Python | 3.10+ | `python3 --version` | [python.org](https://www.python.org/downloads/) |
| Git | any | `git --version` | [git-scm.com](https://git-scm.com/) |

If `python3 --version` shows 3.10 or higher, you're good to go.

## Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/task-manager-cli.git
cd task-manager-cli
```

Replace `<your-username>` with the actual GitHub username or organization.

## Step 2: Create a Virtual Environment

A virtual environment is an isolated Python installation for this project. It keeps project dependencies separate from your system Python, so different projects don't interfere with each other.

```bash
python3 -m venv .venv
```

This creates a `.venv/` folder in the project directory. This folder is already in `.gitignore`, so it won't be committed to Git.

## Step 3: Activate the Virtual Environment

You need to activate the virtual environment every time you open a new terminal window for this project.

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
.venv\Scripts\activate.bat
```

After activation, your terminal prompt should show `(.venv)` at the beginning:

```
(.venv) user@machine task-manager-cli %
```

To deactivate later, just run:

```bash
deactivate
```

## Step 4: Install the Project

```bash
pip install -e .
```

The `-e` flag means "editable" (development mode). With this mode, any changes you make to the source code take effect immediately — no need to reinstall after every edit.

After installation, the `task` command is available in your terminal.

## Step 5: Verify the Installation

```bash
task --help
```

You should see:

```
usage: task [-h] {add,list,done,remove,clear} ...

A simple CLI task manager

positional arguments:
  {add,list,done,remove,clear}
    add                 Add a new task
    list                List all tasks
    done                Mark a task as done
    remove              Remove a task
    clear               Clear all tasks

options:
  -h, --help            show this help message and exit
```

## Step 6: Run the Tests

```bash
pytest -q
```

You should see 29 tests pass:

```
.............................                            [100%]
29 passed in 0.04s
```

Other useful test commands:

```bash
# Verbose output (shows each test name)
pytest -v

# Run a specific test file
pytest tests/test_storage.py -v
pytest tests/test_cli.py -v

# Run a single test function
pytest tests/test_cli.py::test_add_empty_title_fails -v
```

## Step 7: Try the CLI

```bash
# Add some tasks
task add "Read the source code"
task add "Run the tests"

# List all tasks
task list

# Mark a task as done
task done 1

# Filter by status
task list --todo
task list --done

# Remove a task
task remove 2

# Clear all tasks
task clear --yes
```

Your tasks are saved to `tasks.json` in the project root. This file is in `.gitignore` and won't be committed.

## Project Structure

```
task-manager-cli/
├── src/task_manager/
│   ├── __init__.py
│   ├── cli.py          # Entry point — parses CLI args, dispatches to handlers
│   ├── models.py       # Task dataclass with serialization methods
│   └── storage.py      # JSON file I/O: load, save, clear, ID generation
├── tests/
│   ├── test_cli.py     # CLI integration tests (21 tests)
│   └── test_storage.py # Storage unit tests (8 tests)
├── docs/
│   └── dev-setup.md    # This file
├── Dockerfile          # Docker image definition
├── .dockerignore       # Files excluded from Docker build
├── pyproject.toml      # Package metadata and CLI entry point
├── CLAUDE.md           # AI-assisted development guidelines
└── tasks.json          # Local data file (gitignored)
```

**Data flow:**

```
You type a command
  → cli.py (argparse parses the arguments)
  → storage.py (loads tasks from tasks.json)
  → command handler (modifies the task list)
  → storage.py (saves back to tasks.json)
```

## Git Workflow

This project uses feature branches. Here's the typical workflow:

### 1. Start from main

```bash
git checkout main
git pull
```

### 2. Create a feature branch

Branch names follow the pattern `issue-<number>-<short-description>`:

```bash
git checkout -b issue-5-add-search
```

### 3. Make changes and test

```bash
# Edit files...
pytest -v
```

### 4. Commit

Use short, descriptive commit messages. Start with a verb in present tense:

```bash
git add src/task_manager/cli.py tests/test_cli.py
git commit -m "Add task search command"
```

Good commit message examples from this project:
- `Prevent adding empty task titles`
- `Add task list filters`
- `Polish README.md for GitHub portfolio`

### 5. Push and create a Pull Request

```bash
git push -u origin issue-5-add-search
```

Then open a Pull Request on GitHub to merge into `main`.

## Common Issues

### `command not found: task`

The `task` command is not available after `pip install -e .`.

**Cause:** The virtual environment is not activated, or `pip` installed to a different Python.

**Fix:**

```bash
# Make sure the venv is activated
source .venv/bin/activate

# Reinstall
pip install -e .
```

### `ModuleNotFoundError: No module named 'task_manager'`

When running `pytest`, you see this error.

**Cause:** You're running pytest from the wrong directory, or the package isn't installed.

**Fix:**

```bash
# Make sure you're in the project root
cd task-manager-cli

# Make sure the venv is activated
source .venv/bin/activate

# Install the package
pip install -e .

# Run tests
pytest -v
```

### `Permission denied` when activating venv on Windows

**Cause:** PowerShell script execution is restricted.

**Fix:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### `python3` command not found (Windows)

**Cause:** On some Windows systems, Python is installed as `python` instead of `python3`.

**Fix:**

```cmd
python --version
python -m venv .venv
```

### Tests pass locally but CI fails

**Cause:** Not applicable yet — this project does not have CI configured.

## Docker (Optional)

If you have Docker installed, you can build and run the project without setting up a local Python environment.

### Build the image

```bash
docker build -t task-manager .
```

### Run the CLI

```bash
# Show help (default command)
docker run --rm task-manager

# Run a specific command
docker run --rm task-manager task add "Learn Docker"
docker run --rm task-manager task list
```

### Run tests

```bash
docker run --rm task-manager pytest -q
```

You should see:

```
.............................                            [100%]
29 passed in 0.04s
```

### Things to know

- The container is temporary (`--rm` flag deletes it after each run).
- Your local `tasks.json` is not shared with the container. Tasks created inside Docker are lost when the container is removed.
- If you want to persist tasks, mount a volume:

```bash
docker run --rm -v $(pwd)/tasks.json:/app/tasks.json task-manager task add "Persistent task"
```

## Tech Stack Reference

| Component | Choice | Where to Learn More |
|-----------|--------|---------------------|
| Language | Python 3.10+ | [python.org](https://docs.python.org/3/) |
| CLI parsing | `argparse` | [argparse docs](https://docs.python.org/3/library/argparse.html) |
| Data storage | `json` | [json docs](https://docs.python.org/3/library/json.html) |
| Data model | `dataclasses` | [dataclasses docs](https://docs.python.org/3/library/dataclasses.html) |
| File paths | `pathlib` | [pathlib docs](https://docs.python.org/3/library/pathlib.html) |
| Testing | `pytest` | [pytest.org](https://docs.pytest.org/) |
