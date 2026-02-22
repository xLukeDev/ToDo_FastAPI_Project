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


