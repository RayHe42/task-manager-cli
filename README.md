# Task Manager CLI

A simple command-line task manager built with Python. Tasks are stored in a local JSON file.

## Features

- Add, list, complete, and remove tasks
- Clear all tasks at once
- Data stored locally in `tasks.json`
- No external dependencies (Python standard library only)

## Installation

```bash
pip install -e .
```

After installation, the `task` command is available directly in your terminal.

## Usage

```bash
task add "Buy groceries"     # Add a new task
task list                    # List all tasks
task list --todo             # List only incomplete tasks
task list --done             # List only completed tasks
task done 1                  # Mark task 1 as done
task remove 1                # Remove task 1
task clear --yes             # Clear all tasks (requires confirmation)
task --help                  # Show help
```

## Commands

| Command | Description |
|---------|-------------|
| `task add <title>` | Add a new task |
| `task list` | List all tasks |
| `task list --todo` | List only incomplete tasks |
| `task list --done` | List only completed tasks |
| `task done <id>` | Mark a task as done |
| `task remove <id>` | Remove a task |
| `task clear --yes` | Clear all tasks |
| `task --help` | Show help message |

## Running Tests

```bash
pytest
```

## Tech Stack

- Python 3.10+
- argparse (CLI parsing)
- json (data storage)
- pytest (testing)
- pathlib (file paths)

## Project Structure

```
src/task_manager/
├── cli.py          # Entry point, parses CLI arguments (argparse)
├── models.py       # Task data structure
└── storage.py      # Read/write JSON files
tests/
└── test_storage.py # Tests for storage module
```
