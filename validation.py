from datetime import datetime


def validate_task_title(title):
    if not isinstance(title, str) or not title.strip():
        return False, "Task title cannot be empty."
    return True, ""


def validate_task_description(description):
    if not isinstance(description, str) or not description.strip():
        return False, "Task description cannot be empty."
    return True, ""


def validate_due_date(due_date):
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Invalid due date format. Use YYYY-MM-DD."