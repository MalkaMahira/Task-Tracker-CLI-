import argparse
import json
import os
import sys
from datetime import datetime

TASKS_FILE = "tasks.json"


# Ensure the tasks.json file exists and initialize if needed
def ensure_file_exists():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)  # Initialize with an empty list


# Load tasks from tasks.json
def load_tasks():
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            data = file.read()
            if not data.strip():  # Handle empty file
                return []
            return json.loads(data)
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON data in {TASKS_FILE}. Initializing a new file.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading tasks: {e}")
        return []

# Save tasks to JSON file
def save_tasks(tasks):
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except Exception as e:
        print(f"An error occurred while saving tasks: {e}")


# Add a new task
def add_task(description):
    tasks = load_tasks()

    # Create a new task object
    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }

    # Append the new task to the list
    tasks.append(new_task)

    # Save the updated task list to the JSON file
    save_tasks(tasks)

    print(f"Task added: {description}")
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


# Main program logic
def main():
    # Ensure tasks.json exists
    ensure_file_exists()

    # Load tasks from tasks.json
    tasks = load_tasks()

    # Print tasks if available
    if tasks:
        print("Tasks in the tasks.json file:\n")
        for task in tasks:
            print("Entire Task Dictionary:", task)  # Print full dictionary
            print()  # New line for readability
    else:
        print("No tasks found in tasks.json. The file may be empty or improperly formatted.")
    
    # argument parser
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

    # Parse arguments from the command line
    args = parser.parse_args()

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