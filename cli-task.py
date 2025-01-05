import argparse
import json
import os
import sys
from datetime import datetime

# Filepath for the JSON file
TASKS_FILE = "tasks.json"

# Ensure the tasks file exists
def ensure_file_exists():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)

# Load tasks from JSON file
def load_tasks():
    ensure_file_exists()
    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Add a new task
def add_task(description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    now = datetime.now().isoformat()
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now,
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

# Update a task
def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task updated successfully (ID: {task_id})")
            return
    print(f"Task with ID {task_id} not found.")

# Delete a task
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task deleted successfully (ID: {task_id})")

# Mark a task with a specific status
def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status} (ID: {task_id})")
            return
    print(f"Task with ID {task_id} not found.")

# List tasks (with optional status filtering)
def list_tasks(status=None):
    tasks = load_tasks()
    filtered_tasks = tasks if not status else [task for task in tasks if task["status"] == status]
    if not filtered_tasks:
        print("No tasks found.")
    for task in filtered_tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created: {task['createdAt']}, Updated: {task['updatedAt']}")

# CLI entry point
def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add subcommand
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", type=str, help="Task description")

    # Update subcommand
    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("description", type=str, help="New task description")

    # Delete subcommand
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Mark subcommand
    mark_parser = subparsers.add_parser("mark", help="Mark a task")
    mark_parser.add_argument("id", type=int, help="Task ID")
    mark_parser.add_argument("status", choices=["todo", "in-progress", "done"], help="New status")

    # List subcommand
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("status", nargs="?", choices=["todo", "in-progress", "done"], help="Filter by status")

    # Parse arguments
    if get_ipython() is not None:  # If in IPython/Jupyter
        args = parser.parse_args([])  # Parse without sys.argv
    else:  # If running as a standalone script
        args = parser.parse_args(sys.argv[1:])

    # Command execution
    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "mark":
        mark_task(args.id, args.status)
    elif args.command == "list":
        list_tasks(args.status)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
