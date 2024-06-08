from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from backend.app import schemas, models, crud
from backend.app.database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@router.get("/", response_model=List[schemas.Task])
def read_tasks(response: Response, db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    total_tasks = db.query(models.Task).count()
    response.headers["X-Total-Count"] = str(total_tasks)
    print(f"Total tasks: {total_tasks}")
    return tasks

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, completed: bool, db: Session = Depends(get_db)):
    db_task = crud.update_task_status(db=db, task_id=task_id, completed=completed)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
