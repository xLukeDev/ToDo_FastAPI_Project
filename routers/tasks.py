from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime, timezone
from schemas import Task, TaskCreate
import storage
from utils.auth_utils import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

@router.post("/add", response_model=Task)
async def add_task(task_data: TaskCreate, current_user=Depends(get_current_user)):
    new_task = Task(
        id = storage.id_counter,
        user_id= current_user.id,
        **task_data.model_dump()
    )

    storage.tasks_list.append(new_task)
    storage.id_counter += 1

    return new_task

@router.get("", response_model=List[Task])
async def get_all_tasks(current_user=Depends(get_current_user)):
    user_tasks = [task for task in storage.tasks_list if task.user_id==current_user.id]
    return user_tasks

@router.get("/{id}", response_model=Task)
async def get_task_by_id(id: int, current_user=Depends(get_current_user)):

    task = next((task for task in storage.tasks_list if task.id==id and task.user_id == current_user.id), None)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with {id} ID not found")

    return task

@router.patch("/update/mark_finished/{id}", response_model=Task)  #I used patch for updating only specific data (Partial update)
async def task_mark_as_finished(id: int, current_user=Depends(get_current_user)):

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
async def delete_task_by_id(id: int, current_user=Depends(get_current_user)):

    task = next((task for task in storage.tasks_list if task.id==id and task.user_id == current_user.id), None)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with {id} ID not found")

    storage.tasks_list.remove(task)
    return None