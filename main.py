from task_utils import (
    add_task,
    mark_task_as_complete,
    view_pending_tasks,
    calculate_progress
)

def main():
    tasks = []
    while True:
        print("Task Management System")
        print("1. Add Task")
        print("2. Mark Task as Complete")
        print("3. View Pending Tasks")
        print("4. View Progress")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter task due date (YYYY-MM-DD): ")
            priority = input("Enter task priority (low/medium/high or 1-5): ")
            tasks = add_task(tasks, title, description, due_date, priority)
        elif choice == "2":    
            try:
                index = int(input("Enter the index of the task to mark as complete: "))
                tasks = mark_task_as_complete(tasks, index)
            except ValueError:
                print("Invalid index. Please enter a numeric task index.")
        elif choice == "3":    
            view_pending_tasks(tasks)
        elif choice == "4":
            progress = calculate_progress(tasks)
            print(f"Progress: {progress:.2f}%")
        elif choice == "5":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")
        
if __name__ == "__main__":
    main()