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


def test_add_empty_title_fails(capsys):
    """task add "" should reject empty title."""
    with pytest.raises(SystemExit) as exc:
        main(["add", ""])
    assert exc.value.code == 1
    assert "cannot be empty" in capsys.readouterr().err


def test_add_whitespace_only_title_fails(capsys):
    """task add "   " should reject whitespace-only title."""
    with pytest.raises(SystemExit) as exc:
        main(["add", "   "])
    assert exc.value.code == 1
    assert "cannot be empty" in capsys.readouterr().err


def test_add_tab_only_title_fails(capsys):
    """task add with only tab characters should fail."""
    with pytest.raises(SystemExit) as exc:
        main(["add", "\t"])
    assert exc.value.code == 1
    assert "cannot be empty" in capsys.readouterr().err


def test_add_empty_title_does_not_create_task(capsys):
    """Empty title should not create any task."""
    with pytest.raises(SystemExit):
        main(["add", ""])
    main(["list"])
    assert "No tasks." in capsys.readouterr().out


def test_add_title_with_surrounding_spaces_succeeds(capsys):
    """task add "  买菜  " should succeed — strip preserves inner content."""
    main(["add", "  买菜  "])
    out = capsys.readouterr().out
    assert "Added task 1: 买菜" in out


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


def test_list_todo_only(capsys):
    main(["add", "买菜"])
    capsys.readouterr()
    main(["add", "写代码"])
    capsys.readouterr()
    main(["done", "1"])
    capsys.readouterr()
    main(["list", "--todo"])
    out = capsys.readouterr().out
    assert "买菜" not in out
    assert "写代码" in out


def test_list_done_only(capsys):
    main(["add", "买菜"])
    capsys.readouterr()
    main(["add", "写代码"])
    capsys.readouterr()
    main(["done", "1"])
    capsys.readouterr()
    main(["list", "--done"])
    out = capsys.readouterr().out
    assert "买菜" in out
    assert "写代码" not in out


def test_list_todo_empty(capsys):
    main(["add", "买菜"])
    capsys.readouterr()
    main(["done", "1"])
    capsys.readouterr()
    main(["list", "--todo"])
    assert "No tasks." in capsys.readouterr().out


def test_list_done_empty(capsys):
    main(["add", "买菜"])
    capsys.readouterr()
    main(["list", "--done"])
    assert "No tasks." in capsys.readouterr().out


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


# ── TASK_MANAGER_DATA_FILE env var ────────────────────────────────────

def test_env_var_overrides_default_path(monkeypatch, tmp_path):
    """TASK_MANAGER_DATA_FILE env var overrides DEFAULT_TASKS_FILE."""
    custom_path = tmp_path / "custom" / "tasks.json"
    monkeypatch.setenv("TASK_MANAGER_DATA_FILE", str(custom_path))
    main(["add", "环境变量任务"])
    assert custom_path.exists()


def test_env_var_read_write(monkeypatch, tmp_path):
    """Tasks written via env var path can be read back."""
    custom_path = tmp_path / "custom" / "tasks.json"
    monkeypatch.setenv("TASK_MANAGER_DATA_FILE", str(custom_path))
    main(["add", "任务一"])
    # Read back from the same custom path
    from src.task_manager.storage import load_tasks
    tasks = load_tasks(custom_path)
    assert len(tasks) == 1
    assert tasks[0].title == "任务一"


def test_default_path_used_when_env_not_set(monkeypatch):
    """Without TASK_MANAGER_DATA_FILE, DEFAULT_TASKS_FILE is used."""
    monkeypatch.delenv("TASK_MANAGER_DATA_FILE", raising=False)
    # The autouse fixture isolate_tasks_file already redirects DEFAULT_TASKS_FILE
    main(["add", "默认路径任务"])
    main(["list"])
    # Should work normally with the fixture's temp path
