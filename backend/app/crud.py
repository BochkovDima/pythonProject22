from sqlalchemy.orm import Session
from . import models, schemas

# Получение задачи по ID
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# Получение всех задач с поддержкой пагинации
def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()

# Создание новой задачи
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title=task.title, description=task.description, completed=False)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Обновление статуса задачи
def update_task_status(db: Session, task_id: int, completed: bool):
    db_task = get_task(db, task_id)
    if db_task:
        db_task.completed = completed
        db.commit()
        db.refresh(db_task)
    return db_task

# Удаление задачи
def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
