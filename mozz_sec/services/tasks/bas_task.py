from __future__ import annotations

from typing import Any

from pydantic import Field, ConfigDict
from pydantic.alias_generators import to_camel
from pydantic_core import Url

from mozz_sec.data.bas_data import TestDataBas
from mozz_sec.services.tasks.task import BaseExecTask, BaseSubTask, BaseTaskDetail


class SubBasTask(BaseSubTask):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class BasTaskDetail(BaseTaskDetail):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    bas_vm_policy_url: Url
    bas_container_policy_url: Url
    params: TestDataBas = Field(default_factory=TestDataBas, exclude=True)


class BasCleanseTask(BaseTaskDetail):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    bas_vm_policy_url: Url
    bas_container_policy_url: Url


class BasExecTask(BaseExecTask):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    detail: BasTaskDetail = Field(default_factory=BasTaskDetail)

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.task_type = "BAS_EXEC"


class BasExecTaskOut(BasExecTask):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    detail: BasCleanseTask


if __name__ == "__main__":
    task = BasExecTask.model_validate(
        {
            "detail": {
                "bas_vm_policy_url": "http://www.baidu.com",
                "bas_container_policy_url": "http://www.baidu.com",
                "params": {"plugin_set_names": [""], "config": {}, "container_info": {}},
            }
        }
    )
    sub_task_detail = SubBasTask()
    sub_task_detail.progress = 10
    task.detail.details.append(sub_task_detail)
    task.update_progress()
    task.update_status()
    print(task.model_dump_json(indent=4, by_alias=True))
