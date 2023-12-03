from typing import List, Dict

from fastapi import FastAPI, HTTPException, BackgroundTasks
from loguru import logger
from starlette import status

from mozz_sec.services.tasks.bas_task import BasExecTask, BasCleanseTask

app = FastAPI()

TASK_LIST: Dict[str, BasExecTask] = {}


@app.get("/executor/v1/tools/bas/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=BasExecTask)
async def get_task(task_id: str) -> BasExecTask:
    if task_id not in TASK_LIST:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return TASK_LIST[task_id]


@app.post("/executor/v1/tools/bas/tasks/{task_id}", status_code=status.HTTP_201_CREATED, response_model=BasExecTask)
async def create_task(task_id: str, task: BasExecTask, bt: BackgroundTasks) -> BasExecTask:
    logger.info(f"Create Task: {task_id}, {task}")

    if task_id in TASK_LIST:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Task with task_id {task_id} already exists.")

    if not task:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Task is None.")

    task.task_id = task_id
    TASK_LIST[task_id] = task
    bt.add_task(_create_task, task)
    return task


def _create_task(task: BasExecTask):
    logger.info("Run Mozz Sbc Exec Task")
