from pydantic import BaseModel, computed_field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str = None
    description: str = None
    is_done : bool = False
    started_at: datetime
    finished_at: Optional[datetime] = None
    @computed_field
    @property
    def duration_days(self) -> int:

        if not self.finished_at:
            return 0

        return (self.finished_at - self.started_at).days


class Task(TaskCreate):
    id: int
    user_id: int


class User(BaseModel):
    username: str
    email: str | None = None
    full_name : str | None = None
    role: str = 'User'

class UserInDB(User):
    id: int
    hashed_password: str

class UserCreate(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    user_id: int = None

