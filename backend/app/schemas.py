from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    title: str
    description: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    completed: bool

class Task(TaskBase):
    id: int
    completed: bool
    owner_id: Optional[int] = None

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    tasks: List[Task] = []

    class Config:
        from_attributes = True