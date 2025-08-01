# To-Do List Manager

A simple, feature-rich command-line to-do list application built with Python.

## Features

- ✅ Add, remove, and manage tasks
- 📂 Organize tasks by categories
- 🎯 Set task priorities (High, Medium, Low)
- 📅 Set due dates for tasks
- ✓ Mark tasks as complete/incomplete
- 💾 Automatic data persistence with JSON
- 📊 View task statistics
- 🔍 Filter tasks by category and completion status
- 🎨 Colorful, emoji-rich interface

## Installation

1. Clone or download this project
2. Navigate to the project directory
3. Run the application:

```bash
python todo.py
```

## Usage

The application provides an interactive menu with the following options:

1. **Add Task** - Create a new task with title, description, category, priority, and due date
2. **List Tasks** - View all tasks with filtering options
3. **Mark Complete** - Mark a task as completed
4. **Mark Incomplete** - Mark a task as not completed
5. **Remove Task** - Delete a task permanently
6. **View Statistics** - See completion rates and category breakdowns
7. **Filter by Category** - View tasks from specific categories
8. **Exit** - Save and quit the application

## Task Properties

Each task can have:
- **Title** (required) - Brief description of the task
- **Description** (optional) - Detailed information about the task
- **Category** (default: "General") - Organize tasks by type
- **Priority** (default: "Medium") - High, Medium, or Low priority
- **Due Date** (optional) - Target completion date in YYYY-MM-DD format

## Data Storage

Tasks are automatically saved to `tasks.json` in the same directory as the script. This file is created automatically and updated whenever you make changes.

## Example Usage

```
🗂️  TO-DO LIST MANAGER
============================

📋 MENU OPTIONS:
1. ➕ Add Task
2. 📝 List Tasks
3. ✅ Mark Task Complete
4. ❌ Mark Task Incomplete
5. 🗑️  Remove Task
6. 📊 View Statistics
7. 🔍 Filter by Category
8. 🚪 Exit

🔢 Enter your choice (1-8): 1

➕ ADD NEW TASK
----------------
📌 Task title: Buy groceries
📝 Description (optional): Milk, bread, eggs, and vegetables
📂 Category (default: General): Shopping
🎯 Priority (default: Medium): High
📅 Due date (YYYY-MM-DD, optional): 2024-08-02

✅ Task added successfully with ID: 1
```

## File Structure

```
to-do-list/
├── todo.py          # Main application file
├── tasks.json       # Data storage (created automatically)
└── README.md        # This file
```

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

## License

This project is open source and available under the MIT License.
