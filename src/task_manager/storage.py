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


def clear_tasks(path: Path = DEFAULT_TASKS_FILE) -> None:
    """Clear all tasks by writing an empty list."""
    save_tasks([], path)


def next_id(tasks: list[Task]) -> int:
    """Return the next available task ID."""
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1
