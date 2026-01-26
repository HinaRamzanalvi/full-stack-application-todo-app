from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlmodel import Session, select
from middleware.auth import current_user, TokenData
from database.session import get_db as get_db_session
from models.task import Task, TaskRead, TaskCreate, TaskUpdate

router = APIRouter()

@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    status: Optional[str] = None,
    sort: Optional[str] = "created",
    order: Optional[str] = "desc",
    current_user: TokenData = Depends(current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get all tasks for the current user with optional filtering and sorting.
    """
    try:
        print("DEBUG: get_tasks function called")
        # Simple query to test if basic functionality works
        query = select(Task).where(Task.user_id == current_user.user_id)

        result = db.execute(query)
        tasks = result.scalars().all()
        print(f"DEBUG: Retrieved {len(tasks)} tasks")
        return tasks
    except Exception as e:
        print(f"ERROR in get_tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving tasks: {str(e)}")

@router.post("/tasks", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    current_user: TokenData = Depends(current_user),
    db: Session = Depends(get_db_session)
):
    """
    Create a new task for the current user.
    """
    try:
        db_task = Task(
            **task.dict(),
            user_id=current_user.user_id
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        print(f"ERROR in create_task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")

@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    current_user: TokenData = Depends(current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get a specific task by ID for the current user.
    """
    try:
        task = db.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if task.user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this task")

        return task
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        print(f"ERROR in get_task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving task: {str(e)}")

@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: TokenData = Depends(current_user),
    db: Session = Depends(get_db_session)
):
    """
    Update a specific task by ID for the current user.
    """
    try:
        db_task = db.get(Task, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")

        if db_task.user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this task")

        # Update only provided fields
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        print(f"ERROR in update_task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    current_user: TokenData = Depends(current_user),
    db: Session = Depends(get_db_session)
):
    """
    Delete a specific task by ID for the current user.
    """
    try:
        task = db.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if task.user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this task")

        db.delete(task)
        db.commit()
        return {"message": "Task deleted successfully"}
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        print(f"ERROR in delete_task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")

@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    task_id: int,
    current_user: TokenData = Depends(current_user),
    db: Session = Depends(get_db_session)
):
    """
    Toggle the completion status of a specific task for the current user.
    """
    try:
        task = db.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if task.user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this task")

        # Toggle completion status
        task.completed = not task.completed
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        print(f"ERROR in toggle_task_completion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error toggling task completion: {str(e)}")