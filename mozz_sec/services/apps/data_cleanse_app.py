from typing import List, Dict

from fastapi import FastAPI, HTTPException, BackgroundTasks
from loguru import logger
from starlette import status

from mozz_sec.services.tasks.cleanse_task import AnalyseTask
from mozz_sec.services.tasks.sbc_task import SbcCleanseTask
from mozz_sec.services.tasks.bas_task import BasCleanseTask

app = FastAPI()


@app.post("/cleanse/v1/tools/{tool}/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(tool: str, task: AnalyseTask, bt: BackgroundTasks):
    logger.info(f"Create Task: {tool}, {task}")
    logger.error(type(task.data))
    if tool == "bas":
        assert type(task.data) == BasCleanseTask
    elif tool == "sbc":
        assert type(task.data) == SbcCleanseTask
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    bt.add_task(task.data.start_cleanse)
