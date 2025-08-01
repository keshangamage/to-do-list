#!/usr/bin/env python3
"""
Simple To-Do List Application
A command-line to-do list manager with task persistence
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Task:
    """Represents a single task in the to-do list"""
    
    def __init__(self, title: str, description: str = "", category: str = "General", 
                 priority: str = "Medium", due_date: Optional[str] = None):
        self.id = None  # Will be set by TodoList
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def mark_complete(self):
        """Mark the task as completed"""
        self.completed = True
        self.completed_at = datetime.now().isoformat()
    
    def mark_incomplete(self):
        """Mark the task as incomplete"""
        self.completed = False
        self.completed_at = None
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create task from dictionary"""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            category=data.get('category', 'General'),
            priority=data.get('priority', 'Medium'),
            due_date=data.get('due_date')
        )
        task.id = data.get('id')
        task.completed = data.get('completed', False)
        task.created_at = data.get('created_at', datetime.now().isoformat())
        task.completed_at = data.get('completed_at')
        return task
    
    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        priority_symbol = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(self.priority, "🟡")
        
        result = f"{status} [{self.id}] {priority_symbol} {self.title}"
        if self.category != "General":
            result += f" ({self.category})"
        if self.due_date:
            result += f" [Due: {self.due_date}]"
        if self.description:
            result += f"\n    📝 {self.description}"
        
        return result


class TodoList:
    """Main to-do list manager"""
    
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
                    self.next_id = data.get('next_id', 1)
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []
                self.next_id = 1
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        data = {
            'tasks': [task.to_dict() for task in self.tasks],
            'next_id': self.next_id
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_task(self, title: str, description: str = "", category: str = "General", 
                 priority: str = "Medium", due_date: Optional[str] = None) -> Task:
        """Add a new task to the list"""
        task = Task(title, description, category, priority, due_date)
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def remove_task(self, task_id: int) -> bool:
        """Remove a task by ID"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def mark_complete(self, task_id: int) -> bool:
        """Mark a task as complete"""
        task = self.get_task(task_id)
        if task:
            task.mark_complete()
            self.save_tasks()
            return True
        return False
    
    def mark_incomplete(self, task_id: int) -> bool:
        """Mark a task as incomplete"""
        task = self.get_task(task_id)
        if task:
            task.mark_incomplete()
            self.save_tasks()
            return True
        return False
    
    def list_tasks(self, show_completed: bool = True, category: Optional[str] = None) -> List[Task]:
        """List tasks with optional filtering"""
        filtered_tasks = self.tasks
        
        if not show_completed:
            filtered_tasks = [task for task in filtered_tasks if not task.completed]
        
        if category:
            filtered_tasks = [task for task in filtered_tasks if task.category.lower() == category.lower()]
        
        # Sort by completion status, then by priority, then by creation date
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        filtered_tasks.sort(key=lambda t: (
            t.completed,
            priority_order.get(t.priority, 1),
            t.created_at
        ))
        
        return filtered_tasks
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        categories = set(task.category for task in self.tasks)
        return sorted(list(categories))
    
    def get_stats(self) -> Dict:
        """Get task statistics"""
        total = len(self.tasks)
        completed = len([task for task in self.tasks if task.completed])
        pending = total - completed
        
        categories = {}
        for task in self.tasks:
            if task.category not in categories:
                categories[task.category] = {'total': 0, 'completed': 0}
            categories[task.category]['total'] += 1
            if task.completed:
                categories[task.category]['completed'] += 1
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'categories': categories
        }


def print_header():
    """Print application header"""
    print("\n" + "="*60)
    print("🗂️  TO-DO LIST MANAGER")
    print("="*60)


def print_menu():
    """Print main menu options"""
    print("\n📋 MENU OPTIONS:")
    print("1. ➕ Add Task")
    print("2. 📝 List Tasks")
    print("3. ✅ Mark Task Complete")
    print("4. ❌ Mark Task Incomplete")
    print("5. 🗑️  Remove Task")
    print("6. 📊 View Statistics")
    print("7. 🔍 Filter by Category")
    print("8. 🚪 Exit")
    print("-" * 40)


def get_user_input(prompt: str, required: bool = True) -> str:
    """Get user input with validation"""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("❌ This field is required. Please try again.")


def add_task_interactive(todo_list: TodoList):
    """Interactive task addition"""
    print("\n➕ ADD NEW TASK")
    print("-" * 20)
    
    title = get_user_input("📌 Task title: ")
    description = get_user_input("📝 Description (optional): ", required=False)
    
    print("\n📂 Available categories:", ", ".join(todo_list.get_categories()) or "None")
    category = get_user_input("📂 Category (default: General): ", required=False) or "General"
    
    print("\n🎯 Priority levels: High, Medium, Low")
    priority = get_user_input("🎯 Priority (default: Medium): ", required=False) or "Medium"
    if priority.capitalize() not in ["High", "Medium", "Low"]:
        priority = "Medium"
    else:
        priority = priority.capitalize()
    
    due_date = get_user_input("📅 Due date (YYYY-MM-DD, optional): ", required=False) or None
    
    task = todo_list.add_task(title, description, category, priority, due_date)
    print(f"\n✅ Task added successfully with ID: {task.id}")


def list_tasks_interactive(todo_list: TodoList):
    """Interactive task listing"""
    print("\n📝 TASK LIST")
    print("-" * 20)
    
    show_completed = input("Show completed tasks? (y/N): ").lower().startswith('y')
    
    category = get_user_input("Filter by category (optional): ", required=False)
    if category:
        category = category.strip()
    
    tasks = todo_list.list_tasks(show_completed, category)
    
    if not tasks:
        print("📭 No tasks found.")
        return
    
    print(f"\n📋 Found {len(tasks)} task(s):")
    print("-" * 40)
    for task in tasks:
        print(task)
        print()


def mark_task_interactive(todo_list: TodoList, complete: bool):
    """Interactive task completion/incompletion"""
    action = "complete" if complete else "incomplete"
    print(f"\n{'✅' if complete else '❌'} MARK TASK {action.upper()}")
    print("-" * 20)
    
    try:
        task_id = int(get_user_input("🔢 Enter task ID: "))
        success = todo_list.mark_complete(task_id) if complete else todo_list.mark_incomplete(task_id)
        
        if success:
            print(f"✅ Task {task_id} marked as {action}!")
        else:
            print(f"❌ Task {task_id} not found.")
    except ValueError:
        print("❌ Invalid task ID. Please enter a number.")


def remove_task_interactive(todo_list: TodoList):
    """Interactive task removal"""
    print("\n🗑️  REMOVE TASK")
    print("-" * 20)
    
    try:
        task_id = int(get_user_input("🔢 Enter task ID to remove: "))
        task = todo_list.get_task(task_id)
        
        if not task:
            print(f"❌ Task {task_id} not found.")
            return
        
        print(f"\n📋 Task to remove:")
        print(task)
        
        confirm = input("\n⚠️  Are you sure you want to remove this task? (y/N): ")
        if confirm.lower().startswith('y'):
            todo_list.remove_task(task_id)
            print(f"✅ Task {task_id} removed successfully!")
        else:
            print("❌ Task removal cancelled.")
    except ValueError:
        print("❌ Invalid task ID. Please enter a number.")


def show_statistics(todo_list: TodoList):
    """Show task statistics"""
    print("\n📊 TASK STATISTICS")
    print("-" * 20)
    
    stats = todo_list.get_stats()
    
    print(f"📝 Total tasks: {stats['total']}")
    print(f"✅ Completed: {stats['completed']}")
    print(f"⏳ Pending: {stats['pending']}")
    
    if stats['total'] > 0:
        completion_rate = (stats['completed'] / stats['total']) * 100
        print(f"📈 Completion rate: {completion_rate:.1f}%")
    
    if stats['categories']:
        print(f"\n📂 By category:")
        for category, cat_stats in stats['categories'].items():
            completion = (cat_stats['completed'] / cat_stats['total']) * 100 if cat_stats['total'] > 0 else 0
            print(f"   {category}: {cat_stats['completed']}/{cat_stats['total']} ({completion:.1f}%)")


def main():
    """Main application loop"""
    todo_list = TodoList()
    
    print_header()
    print("Welcome to your personal to-do list manager!")
    
    while True:
        print_menu()
        
        try:
            choice = input("🔢 Enter your choice (1-8): ").strip()
            
            if choice == '1':
                add_task_interactive(todo_list)
            elif choice == '2':
                list_tasks_interactive(todo_list)
            elif choice == '3':
                mark_task_interactive(todo_list, True)
            elif choice == '4':
                mark_task_interactive(todo_list, False)
            elif choice == '5':
                remove_task_interactive(todo_list)
            elif choice == '6':
                show_statistics(todo_list)
            elif choice == '7':
                list_tasks_interactive(todo_list)
            elif choice == '8':
                print("\n👋 Thank you for using To-Do List Manager!")
                print("💾 All tasks have been saved automatically.")
                break
            else:
                print("❌ Invalid choice. Please enter a number from 1-8.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
