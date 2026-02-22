from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, computed_field
from datetime import date, datetime, timezone
from typing import List


app = FastAPI()



class TaskCreate(BaseModel):
    title: str = None
    description: str = None
    is_done : bool = False
    started_at: datetime
    finished_at: datetime = None
    @computed_field
    @property
    def duration_days(self) -> int:

        if not self.finished_at:
            return 0

        return (self.finished_at - self.started_at).days


class Task(TaskCreate):
    id: int


tasks_list = []
id_counter = 0

@app.get("/")
async def root():

    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):

    return {"message": f"Hello {name}"}

@app.post("/tasks/add", response_model=Task)
async def add_task(task_data: TaskCreate):

    global id_counter #to change variable that is outside function

    new_task = Task(
        id = id_counter,
        **task_data.model_dump()
    )

    tasks_list.append(new_task)
    id_counter += 1

    return new_task

@app.get("/tasks", response_model=List[Task])
async def get_all_tasks():
    return tasks_list

@app.get("/tasks/{id}", response_model=Task)
async def get_task_by_id(id: int):

    task = next((task for task in tasks_list if task.id==id), None)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with {id} ID not found")

    return task

@app.patch("/taks/update/mark_finished/{id}", response_model=Task)  #I used patch for updating only specific data (Partial update)
async def task_mark_as_finished(id: int):

    global tasks_list

    found_task = None

    for task in tasks_list:
        if task.id == id:
            task.is_done = True
            task.finished_at = datetime.now(timezone.utc)
            found_task = task
            break

    if found_task is None:
        raise HTTPException(status_code=404, detail=f"Task with {id} ID not found")

    return found_task


@app.delete("/task/delete/{id}", response_model=Task)
async def delete_task_by_id(id: int):

    task = next((task for task in tasks_list if task.id==id), None)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with {id} ID not found")

    tasks_list.remove(task)