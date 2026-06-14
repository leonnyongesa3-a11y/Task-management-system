from datetime import datetime
from validation import validate_task_title, validate_task_description, validate_due_date, validate_priority

def add_task(tasks, title, description, due_date, priority):
    try:
        validate_task_title(title)
        validate_task_description(description)
        validate_due_date(due_date)
        validate_priority(priority)
    except ValueError as e:
        print(str(e))
        return tasks

    task = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "priority": priority,
        "status": "pending"
    }
    tasks.append(task)
    print("Task added successfully!")
    return tasks
    
def mark_task_as_complete(tasks, index):
    zero_index = index - 1
    if 0 <= zero_index < len(tasks):
        tasks[zero_index]["status"] = "complete"
        print("Task marked as complete!")
    else:
        print("Invalid task index. Please enter a valid index.")
    return tasks
    
def view_pending_tasks(tasks):
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    for task in pending_tasks:
        print(f"Title: {task['title']}, Description: {task['description']}, Due Date: {task['due_date']}")

def calculate_progress(tasks):
    total_tasks = len(tasks)
    if total_tasks == 0:
        return 0.0
    completed_tasks = len([task for task in tasks if task.get("status") == "complete" or task.get("completed") == True])
    return (completed_tasks / total_tasks * 100)