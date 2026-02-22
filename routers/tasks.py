from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime, timezone
from schemas import Task, TaskCreate
import storage


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@router.post("/add", response_model=Task)
async def add_task(task_data: TaskCreate):
    new_task = Task(
        id = storage.id_counter,
        **task_data.model_dump()
    )

    storage.tasks_list.append(new_task)
    storage.id_counter += 1

    return new_task

@router.get("", response_model=List[Task])
async def get_all_tasks():
    return storage.tasks_list

@router.get("/{id}", response_model=Task)
async def get_task_by_id(id: int):

    task = next((task for task in storage.tasks_list if task.id==id), None)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with {id} ID not found")

    return task

@router.patch("/update/mark_finished/{id}", response_model=Task)  #I used patch for updating only specific data (Partial update)
async def task_mark_as_finished(id: int):

    found_task = None
    for task in storage.tasks_list:
        if task.id == id:
            task.is_done = True
            task.finished_at = datetime.now(timezone.utc)
            found_task = task
            break

    if found_task is None:
        raise HTTPException(status_code=404, detail=f"Task with {id} ID not found")

    return found_task


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_id(id: int):

    task = next((task for task in storage.tasks_list if task.id==id), None)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with {id} ID not found")

    storage.tasks_list.remove(task)
    return None