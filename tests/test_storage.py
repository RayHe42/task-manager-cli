import json
import pytest
from pathlib import Path

from src.task_manager.models import Task
from src.task_manager.storage import load_tasks, save_tasks, clear_tasks, next_id


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


def test_clear_tasks(tmp_tasks_file):
    """clear_tasks removes all tasks."""
    save_tasks([Task(1, "a"), Task(2, "b")], tmp_tasks_file)
    clear_tasks(tmp_tasks_file)
    loaded = load_tasks(tmp_tasks_file)
    assert loaded == []


def test_clear_tasks_empty_file(tmp_tasks_file):
    """clear_tasks on empty file still results in empty list."""
    clear_tasks(tmp_tasks_file)
    loaded = load_tasks(tmp_tasks_file)
    assert loaded == []


def test_next_id_empty():
    """next_id returns 1 for empty list."""
    assert next_id([]) == 1


def test_next_id_with_tasks():
    """next_id returns max id + 1."""
    tasks = [Task(1, "a"), Task(3, "b"), Task(2, "c")]
    assert next_id(tasks) == 4
