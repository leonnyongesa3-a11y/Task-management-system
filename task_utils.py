from operator import index

from validation import (
    validate_task_title,
    validate_task_description,
    validate_due_date
)

tasks = []


def add_task(title, description, due_date):
    valid, msg = validate_task_title(title)
    if not valid:
        print(msg)
        return

    valid, msg = validate_task_description(description)
    if not valid:
        print(msg)
        return

    valid, msg = validate_due_date(due_date)
    if not valid:
        print(msg)
        return

    task = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False
    }

    tasks.append(task)
    print("Task added successfully!")


def mark_task_as_complete(index):
    index = index - 1  

    if index < 0 or index >= len(tasks):
        print("Invalid task index.")
        return

    tasks[index]["completed"] = True
    print("Task marked as complete!")


def view_pending_tasks():
    pending = [t for t in tasks if not t["completed"]]

    if not pending:
        print("No pending tasks.")
        return

    print("\nPending Tasks:")
    for i, task in enumerate(pending, start=1):
        print(f"{i}. {task['title']} (Due: {task['due_date']})")


def calculate_progress():
    if len(tasks) == 0:
        return 0

    completed = sum(1 for t in tasks if t["completed"])
    return (completed / len(tasks)) * 100