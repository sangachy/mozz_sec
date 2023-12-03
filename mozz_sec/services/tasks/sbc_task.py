from __future__ import annotations
from pathlib import Path
from typing import Any

from pydantic import Field, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from mozz_sec.data.sbc_data import TestDataSbc, ScanType
from mozz_sec.services._types import TaskStatus
from mozz_sec.services.tasks.task import BaseExecTask, BaseSubTask, BaseTaskDetail


class SubSbcTask(BaseSubTask):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    file_path: Path = Field(default="", alias="file", exclude=True)


class SbcCleanseData(TestDataSbc):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    username: str
    password: str


class SbcCleanseTask(BaseTaskDetail):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    params: SbcCleanseData


class SbcExecTask(BaseExecTask):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    detail: SbcCleanseTask

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.task_type = "SBC_EXEC"


if __name__ == "__main__":
    task = SbcExecTask.model_validate(
        {
            "detail": {
                "params": {
                    "username": "p_mozzps",
                    "password": "Huawei12#$",
                    "url-list": ["https://www.baidu.com"],
                    "scan-type": {"binscope": True},
                }
            }
        }
    )
    task.progress = 100
    task.status = TaskStatus.Finished
    task.message = "Test"
    task.task_id = "taskid"
    task.detail.secguard_workspace_url = "http://secguard.rnd.huawei.com"
    print(task.detail.params)
    sub_task_detail = SubSbcTask()
    task.detail = SbcCleanseTask(details=[sub_task_detail], params=task.detail.params)
    print(task.model_dump_json(indent=4, by_alias=True))
