import argparse
import sys
from pathlib import Path

from .storage import load_tasks, save_tasks, clear_tasks, next_id, DEFAULT_TASKS_FILE


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task",
        description="A simple CLI task manager",
    )
    subparsers = parser.add_subparsers(dest="command")

    # task add "title"
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")

    # task list [--todo | --done]
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_group = list_parser.add_mutually_exclusive_group()
    list_group.add_argument("--todo", action="store_true", help="Show only incomplete tasks")
    list_group.add_argument("--done", action="store_true", help="Show only completed tasks")

    # task done <id>
    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, help="Task ID")

    # task remove <id>
    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("id", type=int, help="Task ID")

    # task clear [--yes]
    clear_parser = subparsers.add_parser("clear", help="Clear all tasks")
    clear_parser.add_argument("--yes", action="store_true", help="Confirm clear")

    return parser


def cmd_add(args, tasks, path):
    task_id = next_id(tasks)
    from .models import Task
    tasks.append(Task(id=task_id, title=args.title))
    save_tasks(tasks, path)
    print(f"Added task {task_id}: {args.title}")


def cmd_list(args, tasks, path):
    filtered = tasks
    if args.todo:
        filtered = [t for t in tasks if not t.done]
    elif args.done:
        filtered = [t for t in tasks if t.done]

    if not filtered:
        print("No tasks.")
        return
    for task in filtered:
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


def cmd_clear(args, tasks, path):
    if not args.yes:
        print("Use 'task clear --yes' to confirm.")
        return
    clear_tasks(path)
    print("All tasks cleared.")


COMMANDS = {
    "add": cmd_add,
    "list": cmd_list,
    "done": cmd_done,
    "remove": cmd_remove,
    "clear": cmd_clear,
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
