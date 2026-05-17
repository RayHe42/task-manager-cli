import pytest

from src.task_manager.cli import main
from src.task_manager.storage import DEFAULT_TASKS_FILE


@pytest.fixture(autouse=True)
def isolate_tasks_file(tmp_path, monkeypatch):
    """Redirect all CLI file I/O to a temp directory."""
    monkeypatch.setattr(
        "src.task_manager.cli.DEFAULT_TASKS_FILE",
        tmp_path / "tasks.json",
    )


# ── add ──────────────────────────────────────────────────────────────

def test_add_single_task(capsys):
    main(["add", "买菜"])
    out = capsys.readouterr().out
    assert "Added task 1: 买菜" in out


def test_add_multiple_tasks_increments_id(capsys):
    main(["add", "买菜"])
    main(["add", "写代码"])
    out = capsys.readouterr().out
    assert "Added task 1" in out
    assert "Added task 2" in out


# ── list ─────────────────────────────────────────────────────────────

def test_list_empty(capsys):
    main(["list"])
    assert "No tasks." in capsys.readouterr().out


def test_list_shows_tasks(capsys):
    main(["add", "买菜"])
    capsys.readouterr()  # drain
    main(["done", "1"])
    capsys.readouterr()  # drain
    main(["add", "写代码"])
    capsys.readouterr()  # drain
    main(["list"])
    lines = capsys.readouterr().out.strip().splitlines()
    assert "[✓] 1. 买菜" in lines[0]
    assert "[ ] 2. 写代码" in lines[1]


# ── done ─────────────────────────────────────────────────────────────

def test_done_existing_task(capsys):
    main(["add", "买菜"])
    main(["done", "1"])
    assert "Marked task 1 as done." in capsys.readouterr().out


def test_done_nonexistent_task(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["done", "99"])
    assert exc.value.code == 1
    assert "not found" in capsys.readouterr().err


# ── remove ───────────────────────────────────────────────────────────

def test_remove_existing_task(capsys):
    main(["add", "买菜"])
    main(["remove", "1"])
    assert "Removed task 1." in capsys.readouterr().out


def test_remove_nonexistent_task(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["remove", "99"])
    assert exc.value.code == 1
    assert "not found" in capsys.readouterr().err


# ── clear ────────────────────────────────────────────────────────────

def test_clear_without_yes(capsys):
    main(["add", "买菜"])
    main(["clear"])
    assert "Use 'task clear --yes'" in capsys.readouterr().out

    # Tasks should still be there
    main(["list"])
    assert "买菜" in capsys.readouterr().out


def test_clear_with_yes(capsys):
    main(["add", "买菜"])
    main(["clear", "--yes"])
    assert "All tasks cleared." in capsys.readouterr().out

    # List should be empty
    main(["list"])
    assert "No tasks." in capsys.readouterr().out


# ── edge cases ───────────────────────────────────────────────────────

def test_done_then_list_reflects_change(capsys):
    """done + list together work correctly."""
    main(["add", "买菜"])
    main(["done", "1"])
    main(["list"])
    assert "[✓]" in capsys.readouterr().out


def test_remove_then_list_reflects_change(capsys):
    """remove + list together work correctly."""
    main(["add", "买菜"])
    capsys.readouterr()  # drain
    main(["add", "写代码"])
    capsys.readouterr()  # drain
    main(["remove", "1"])
    capsys.readouterr()  # drain
    main(["list"])
    out = capsys.readouterr().out
    assert "买菜" not in out
    assert "写代码" in out
