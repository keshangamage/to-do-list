#!/usr/bin/env python3
"""
Example usage of the TodoList class
This script demonstrates how to use the to-do list programmatically
"""

from todo import TodoList, Task

def main():
    # Create a new to-do list instance
    todo = TodoList("example_tasks.json")
    
    print("🚀 To-Do List API Example")
    print("=" * 30)
    
    # Add some sample tasks
    print("\n📝 Adding sample tasks...")
    
    task1 = todo.add_task(
        title="Learn Python",
        description="Complete a Python tutorial and build a project",
        category="Education",
        priority="High",
        due_date="2024-08-15"
    )
    
    task2 = todo.add_task(
        title="Buy groceries",
        description="Milk, bread, eggs, vegetables",
        category="Shopping",
        priority="Medium",
        due_date="2024-08-02"
    )
    
    task3 = todo.add_task(
        title="Exercise",
        description="30-minute workout",
        category="Health",
        priority="High"
    )
    
    task4 = todo.add_task(
        title="Read a book",
        description="Finish reading 'The Python Crash Course'",
        category="Education",
        priority="Low"
    )
    
    print(f"✅ Added {len(todo.tasks)} tasks")
    
    # List all tasks
    print("\n📋 All tasks:")
    print("-" * 40)
    for task in todo.list_tasks():
        print(task)
        print()
    
    # Mark some tasks as complete
    print("✅ Marking task 2 as complete...")
    todo.mark_complete(2)
    
    print("✅ Marking task 3 as complete...")
    todo.mark_complete(3)
    
    # Show only pending tasks
    print("\n⏳ Pending tasks:")
    print("-" * 40)
    pending_tasks = todo.list_tasks(show_completed=False)
    for task in pending_tasks:
        print(task)
        print()
    
    # Show tasks by category
    print("\n📚 Education tasks:")
    print("-" * 40)
    education_tasks = todo.list_tasks(category="Education")
    for task in education_tasks:
        print(task)
        print()
    
    # Show statistics
    print("\n📊 Statistics:")
    print("-" * 20)
    stats = todo.get_stats()
    print(f"Total tasks: {stats['total']}")
    print(f"Completed: {stats['completed']}")
    print(f"Pending: {stats['pending']}")
    
    if stats['total'] > 0:
        completion_rate = (stats['completed'] / stats['total']) * 100
        print(f"Completion rate: {completion_rate:.1f}%")
    
    print(f"\nCategories: {', '.join(todo.get_categories())}")
    
    # Remove a task
    print(f"\n🗑️ Removing task 4...")
    todo.remove_task(4)
    
    print(f"\n📊 Final statistics:")
    final_stats = todo.get_stats()
    print(f"Total tasks: {final_stats['total']}")
    print(f"Completed: {final_stats['completed']}")
    print(f"Pending: {final_stats['pending']}")
    
    print("\n💾 All changes saved to example_tasks.json")
    print("🎉 Example completed!")

if __name__ == "__main__":
    main()
