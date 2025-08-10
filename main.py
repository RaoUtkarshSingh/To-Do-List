import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(tasks):
    task = input("Enter a new task: ").strip()
    priority = input("Set priority (High, Medium, Low) [Medium]: ").capitalize()
    if priority not in ["High", "Medium", "Low"]:
        priority = "Medium"
    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ").strip()
    # Validate date
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Due date will be empty.")
            due_date = ""
    tasks.append({"task": task, "done": False, "priority": priority, "due_date": due_date})
    print("Task added!")

def view_tasks(tasks, filter_status="all"):
    if not tasks:
        print("No tasks found.")
        return
    
    filtered = []
    if filter_status == "pending":
        filtered = [t for t in tasks if not t["done"]]
    elif filter_status == "done":
        filtered = [t for t in tasks if t["done"]]
    else:
        filtered = tasks

    if not filtered:
        print(f"No {filter_status} tasks found.")
        return

    today = datetime.today().date()
    for idx, t in enumerate(filtered, 1):
        status = "✓" if t["done"] else "✗"
        due_str = t["due_date"]
        overdue = False
        if due_str:
            due_date_obj = datetime.strptime(due_str, "%Y-%m-%d").date()
            if due_date_obj < today and not t["done"]:
                overdue = True
        overdue_str = " (Overdue!)" if overdue else ""
        print(f"{idx}. [{status}] {t['task']} | Priority: {t['priority']} | Due: {due_str if due_str else 'N/A'}{overdue_str}")

def select_task(tasks, filter_status="all"):
    # Helper function to select a task by filtered index
    filtered = []
    if filter_status == "pending":
        filtered = [t for t in tasks if not t["done"]]
    elif filter_status == "done":
        filtered = [t for t in tasks if t["done"]]
    else:
        filtered = tasks

    if not filtered:
        print("No tasks to select.")
        return None, None

    view_tasks(tasks, filter_status)
    try:
        task_num = int(input("Enter task number: "))
        if 1 <= task_num <= len(filtered):
            selected_task = filtered[task_num - 1]
            # Find index in original list
            original_index = tasks.index(selected_task)
            return original_index, selected_task
        else:
            print("Invalid task number.")
            return None, None
    except ValueError:
        print("Please enter a valid number.")
        return None, None

def mark_done(tasks):
    idx, task = select_task(tasks, "pending")
    if idx is not None:
        tasks[idx]["done"] = True
        print(f"Marked '{task['task']}' as done.")

def delete_task(tasks):
    idx, task = select_task(tasks)
    if idx is not None:
        removed = tasks.pop(idx)
        print(f"Deleted task: {removed['task']}")

def edit_task(tasks):
    idx, task = select_task(tasks)
    if idx is not None:
        print(f"Current task: {task['task']}")
        new_task = input("Enter new task text (leave blank to keep unchanged): ").strip()
        if new_task:
            tasks[idx]["task"] = new_task
        print(f"Current priority: {task['priority']}")
        new_priority = input("Enter new priority (High, Medium, Low) or leave blank: ").capitalize()
        if new_priority in ["High", "Medium", "Low"]:
            tasks[idx]["priority"] = new_priority
        print(f"Current due date: {task['due_date'] if task['due_date'] else 'N/A'}")
        new_due = input("Enter new due date (YYYY-MM-DD) or leave blank: ").strip()
        if new_due:
            try:
                datetime.strptime(new_due, "%Y-%m-%d")
                tasks[idx]["due_date"] = new_due
            except ValueError:
                print("Invalid date format. Due date unchanged.")
        print("Task updated!")

def clear_completed(tasks):
    before_count = len(tasks)
    tasks[:] = [t for t in tasks if not t["done"]]
    removed_count = before_count - len(tasks)
    print(f"Removed {removed_count} completed tasks.")

def main():
    tasks = load_tasks()

    while True:
        print("\n--- To-Do List ---")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Completed Tasks")
        print("5. Mark Task Done")
        print("6. Edit Task")
        print("7. Delete Task")
        print("8. Clear All Completed Tasks")
        print("9. Exit")

        choice = input("Choose an option (1-9): ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks, "all")
        elif choice == "3":
            view_tasks(tasks, "pending")
        elif choice == "4":
            view_tasks(tasks, "done")
        elif choice == "5":
            mark_done(tasks)
        elif choice == "6":
            edit_task(tasks)
        elif choice == "7":
            delete_task(tasks)
        elif choice == "8":
            clear_completed(tasks)
        elif choice == "9":
            save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

        save_tasks(tasks)

if __name__ == "__main__":
    main()
