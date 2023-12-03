from typing import List, Any

from loguru import logger
from pydantic import BaseModel, Field

from mozz_sec.services.tasks.task import BaseSubTask, BaseExecTask


class SubRunner(BaseModel):
    name: str
    task: BaseSubTask

    def run_task(self):
        logger.debug(f"[{self.name}]Run Task")


class BaseRunner(BaseModel):
    task: BaseExecTask
    sub_runners: List[SubRunner] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        for sub_task in task.detail.details:
            self.sub_runners.append(SubRunner(name=task.task_id, task=sub_task))

    def run_task(self):
        for _runner in self.sub_runners:
            _runner.run_task()


if __name__ == "__main__":
    sub_task = BaseSubTask()
    sub_task.task_id = "1"
    task = BaseExecTask()
    task.detail.details.append(sub_task)

    runner = BaseRunner(task=task)
    runner.run_task()
