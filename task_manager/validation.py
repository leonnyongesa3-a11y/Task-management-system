from datetime import datetime
 
def validate_task_title(title):
    if len(title.strip()) == 0:
        raise ValueError("Task title cannot be empty.")
    return True
    
def validate_task_description(description):
    if len(description.strip()) == 0:
        raise ValueError("Task description cannot be empty.")
    if len(description) > 500:
        raise ValueError("Task description cannot exceed 500 characters.")
    return True
 
def validate_due_date(due_date):
    if len(due_date.strip()) == 0:
        raise ValueError("Due date cannot be empty.")
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
        return True
    except ValueError:
        raise ValueError("Due date must be in YYYY-MM-DD format.")

def validate_priority(priority):
    priority_text = str(priority).strip().lower()
    valid_text_priorities = {"low", "medium", "high"}
    if priority_text in valid_text_priorities:
        return True
    try:
        p = int(priority)
        if 1 <= p <= 5:
            return True
        else:
            raise ValueError("Priority must be between 1 and 5.")
    except ValueError:
        raise ValueError("Priority must be low, medium, high, or 1-5.")