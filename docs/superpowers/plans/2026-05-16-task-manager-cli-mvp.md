# Task Manager CLI MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python CLI task manager that stores tasks in a local JSON file, with add/list/done/remove commands.

**Architecture:** Three-layer design: `models.py` defines the Task data structure, `storage.py` handles JSON file I/O, and `cli.py` wires argparse to storage. Tests cover storage logic (the core read/write path). A `setup.py` enables `pip install -e .` for the `task` entry point.

**Tech Stack:** Python 3.10+ standard library only (argparse, json, pathlib, dataclasses). pytest for testing.

---

## File Structure

```
src/task_manager/
├── __init__.py      # Package init (empty or minimal)
├── models.py        # Task dataclass
├── storage.py       # JSON file read/write
└── cli.py           # argparse entry point
tests/
├── test_storage.py  # Tests for storage.py
└── __init__.py      # Empty, makes tests a package
setup.py             # Package config with console_scripts entry point
```

---

### Task 1: Task Data Model (`models.py`)

**Files:**
- Modify: `src/task_manager/models.py`

- [ ] **Step 1: Define Task dataclass**

```python
from dataclasses import dataclass, asdict


@dataclass
class Task:
    id: int
    title: str
    done: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(id=data["id"], title=data["title"], done=data["done"])
```

- [ ] **Step 2: Verify it works**

Run: `python -c "from src.task_manager.models import Task; t = Task(1, 'test'); print(t.to_dict())"`
Expected: `{'id': 1, 'title': 'test', 'done': False}`

---

### Task 2: Storage Layer (`storage.py`) — TDD

**Files:**
- Modify: `tests/test_storage.py`
- Modify: `src/task_manager/storage.py`

- [ ] **Step 1: Write failing tests for storage**

```python
import json
import pytest
from pathlib import Path

from src.task_manager.models import Task
from src.task_manager.storage import load_tasks, save_tasks, next_id


@pytest.fixture
def tmp_tasks_file(tmp_path):
    """Return a temporary tasks.json path."""
    return tmp_path / "tasks.json"


def test_load_tasks_empty(tmp_tasks_file):
    """Loading from nonexistent file returns empty list."""
    tasks = load_tasks(tmp_tasks_file)
    assert tasks == []


def test_save_and_load(tmp_tasks_file):
    """Saved tasks can be loaded back."""
    tasks = [Task(1, "买菜"), Task(2, "写代码", done=True)]
    save_tasks(tasks, tmp_tasks_file)

    loaded = load_tasks(tmp_tasks_file)
    assert len(loaded) == 2
    assert loaded[0].id == 1
    assert loaded[0].title == "买菜"
    assert loaded[0].done is False
    assert loaded[1].id == 2
    assert loaded[1].done is True


def test_save_creates_parent_dirs(tmp_path):
    """save_tasks creates parent directories if needed."""
    path = tmp_path / "subdir" / "tasks.json"
    save_tasks([Task(1, "test")], path)
    assert path.exists()


def test_load_corrupt_json(tmp_tasks_file):
    """Loading corrupt JSON raises ValueError."""
    tmp_tasks_file.write_text("not valid json")
    with pytest.raises(ValueError, match="Invalid JSON"):
        load_tasks(tmp_tasks_file)


def test_next_id_empty():
    """next_id returns 1 for empty list."""
    assert next_id([]) == 1


def test_next_id_with_tasks():
    """next_id returns max id + 1."""
    tasks = [Task(1, "a"), Task(3, "b"), Task(2, "c")]
    assert next_id(tasks) == 4
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/rayhe/dev/ai-enginner-lab/task-manager-cli && python -m pytest tests/test_storage.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'src.task_manager.storage'`

- [ ] **Step 3: Implement storage.py**

```python
import json
from pathlib import Path

from .models import Task

DEFAULT_TASKS_FILE = Path("tasks.json")


def load_tasks(path: Path = DEFAULT_TASKS_FILE) -> list[Task]:
    """Load tasks from a JSON file. Returns empty list if file doesn't exist."""
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}") from e
    return [Task.from_dict(item) for item in data]


def save_tasks(tasks: list[Task], path: Path = DEFAULT_TASKS_FILE) -> None:
    """Save tasks to a JSON file, creating parent dirs if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [task.to_dict() for task in tasks]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def next_id(tasks: list[Task]) -> int:
    """Return the next available task ID."""
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/rayhe/dev/ai-enginner-lab/task-manager-cli && python -m pytest tests/test_storage.py -v`
Expected: All 6 tests PASS

---

### Task 3: CLI Entry Point (`cli.py`)

**Files:**
- Modify: `src/task_manager/cli.py`
- Modify: `src/task_manager/__init__.py`

- [ ] **Step 1: Implement cli.py with argparse**

```python
import argparse
import sys
from pathlib import Path

from .storage import load_tasks, save_tasks, next_id, DEFAULT_TASKS_FILE


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task",
        description="A simple CLI task manager",
    )
    subparsers = parser.add_subparsers(dest="command")

    # task add "title"
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")

    # task list
    subparsers.add_parser("list", help="List all tasks")

    # task done <id>
    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, help="Task ID")

    # task remove <id>
    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("id", type=int, help="Task ID")

    return parser


def cmd_add(args, tasks, path):
    task_id = next_id(tasks)
    from .models import Task
    tasks.append(Task(id=task_id, title=args.title))
    save_tasks(tasks, path)
    print(f"Added task {task_id}: {args.title}")


def cmd_list(args, tasks, path):
    if not tasks:
        print("No tasks.")
        return
    for task in tasks:
        status = "✓" if task.done else " "
        print(f"  [{status}] {task.id}. {task.title}")


def cmd_done(args, tasks, path):
    for task in tasks:
        if task.id == args.id:
            task.done = True
            save_tasks(tasks, path)
            print(f"Marked task {args.id} as done.")
            return
    print(f"Task {args.id} not found.", file=sys.stderr)
    sys.exit(1)


def cmd_remove(args, tasks, path):
    original_len = len(tasks)
    tasks = [t for t in tasks if t.id != args.id]
    if len(tasks) == original_len:
        print(f"Task {args.id} not found.", file=sys.stderr)
        sys.exit(1)
    save_tasks(tasks, path)
    print(f"Removed task {args.id}.")


COMMANDS = {
    "add": cmd_add,
    "list": cmd_list,
    "done": cmd_done,
    "remove": cmd_remove,
}


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    path = DEFAULT_TASKS_FILE
    tasks = load_tasks(path)
    COMMANDS[args.command](args, tasks, path)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Set up __init__.py**

```python
from .models import Task
from .storage import load_tasks, save_tasks
```

- [ ] **Step 3: Verify CLI runs without errors**

Run: `cd /Users/rayhe/dev/ai-enginner-lab/task-manager-cli && python -m src.task_manager.cli`
Expected: Shows help message (argparse default)

---

### Task 4: Package Setup (`setup.py`)

**Files:**
- Create: `setup.py`

- [ ] **Step 1: Create setup.py**

```python
from setuptools import setup, find_packages

setup(
    name="task-manager-cli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "task=task_manager.cli:main",
        ],
    },
    python_requires=">=3.10",
)
```

- [ ] **Step 2: Install in development mode**

Run: `cd /Users/rayhe/dev/ai-enginner-lab/task-manager-cli && pip install -e .`
Expected: Successfully installs with `task` command available

- [ ] **Step 3: Verify the `task` command works**

Run: `task --help`
Expected: Shows argparse help with add/list/done/remove subcommands

---

### Task 5: Create tests/__init__.py

**Files:**
- Create: `tests/__init__.py`

- [ ] **Step 1: Create empty __init__.py**

```python
```

(Empty file — makes `tests` a proper Python package for import resolution.)

---

### Task 6: Integration Verification

- [ ] **Step 1: Run full test suite**

Run: `cd /Users/rayhe/dev/ai-enginner-lab/task-manager-cli && python -m pytest tests/ -v`
Expected: All 6 tests PASS

- [ ] **Step 2: Manual smoke test**

Run these commands and verify output:

```bash
# Clean start
rm -f tasks.json

# Add tasks
task add "买菜"
# Expected: Added task 1: 买菜

task add "写代码"
# Expected: Added task 2: 写代码

# List tasks
task list
# Expected:
#   [ ] 1. 买菜
#   [ ] 2. 写代码

# Mark done
task done 1
# Expected: Marked task 1 as done.

task list
# Expected:
#   [✓] 1. 买菜
#   [ ] 2. 写代码

# Remove task
task remove 2
# Expected: Removed task 2.

task list
# Expected:
#   [✓] 1. 买菜

# Error cases
task done 99
# Expected: Task 99 not found. (exit code 1)

task remove 99
# Expected: Task 99 not found. (exit code 1)

# Check JSON file
cat tasks.json
# Expected: JSON with one task, id=1, done=true
```

---

## Notes

- **No auto-commit** per project rules — user decides when to commit.
- **No third-party dependencies** — only stdlib + pytest.
- **Default file** is `tasks.json` in the current working directory.
- **Error handling** is minimal as befits an MVP — corrupt JSON raises ValueError, missing IDs print to stderr and exit 1.
