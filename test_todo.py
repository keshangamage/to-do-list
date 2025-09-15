#!/usr/bin/env python3
"""
Simple tests for the To-Do List application
Run with: python test_todo.py
"""

import os
import json
import tempfile
from todo import TodoList, Task

def test_task_creation():
    """Test creating a task"""
    print("🧪 Testing task creation...")
    task = Task("Test task", "Test description", "Test", "High", "2024-12-31")
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.category == "Test"
    assert task.priority == "High"
    assert task.due_date == "2024-12-31"
    assert not task.completed
    print("✅ Task creation test passed!")

def test_task_completion():
    """Test marking tasks complete/incomplete"""
    print("🧪 Testing task completion...")
    task = Task("Test task")
    assert not task.completed
    
    task.mark_complete()
    assert task.completed
    assert task.completed_at is not None
    
    task.mark_incomplete()
    assert not task.completed
    assert task.completed_at is None
    print("✅ Task completion test passed!")

def test_todolist_operations():
    """Test TodoList operations"""
    print("🧪 Testing TodoList operations...")
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        # Test creating and adding tasks
        todo = TodoList(temp_file)
        
        task1 = todo.add_task("Task 1", "Description 1", "Work", "High")
        task2 = todo.add_task("Task 2", "Description 2", "Personal", "Low")
        
        assert len(todo.tasks) == 2
        assert task1.id == 1
        assert task2.id == 2
        
        # Test marking complete
        assert todo.mark_complete(1)
        assert todo.get_task(1).completed
        
        # Test listing tasks
        all_tasks = todo.list_tasks()
        assert len(all_tasks) == 2
        
        pending_tasks = todo.list_tasks(show_completed=False)
        assert len(pending_tasks) == 1
        assert pending_tasks[0].id == 2
        
        # Test filtering by category
        work_tasks = todo.list_tasks(category="Work")
        assert len(work_tasks) == 1
        assert work_tasks[0].category == "Work"
        
        # Test removing task
        assert todo.remove_task(2)
        assert len(todo.tasks) == 1
        assert not todo.remove_task(999) 
        
        # Test statistics
        stats = todo.get_stats()
        assert stats['total'] == 1
        assert stats['completed'] == 1
        assert stats['pending'] == 0
        
        # Test persistence
        todo2 = TodoList(temp_file)
        assert len(todo2.tasks) == 1
        assert todo2.tasks[0].title == "Task 1"
        assert todo2.tasks[0].completed
        
        print("✅ TodoList operations test passed!")
        
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def test_task_serialization():
    """Test task to_dict and from_dict methods"""
    print("🧪 Testing task serialization...")
    
    original_task = Task("Test task", "Description", "Category", "High", "2024-12-31")
    original_task.id = 1
    original_task.mark_complete()
    
    # Convert to dict and back
    task_dict = original_task.to_dict()
    restored_task = Task.from_dict(task_dict)
    
    assert restored_task.id == original_task.id
    assert restored_task.title == original_task.title
    assert restored_task.description == original_task.description
    assert restored_task.category == original_task.category
    assert restored_task.priority == original_task.priority
    assert restored_task.due_date == original_task.due_date
    assert restored_task.completed == original_task.completed
    assert restored_task.completed_at == original_task.completed_at
    
    print("✅ Task serialization test passed!")

def run_all_tests():
    """Run all tests"""
    print("🚀 Running To-Do List Tests")
    print("=" * 30)
    
    try:
        test_task_creation()
        test_task_completion()
        test_task_serialization()
        test_todolist_operations()
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
