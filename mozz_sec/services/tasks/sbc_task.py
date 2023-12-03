from __future__ import annotations
from pathlib import Path
from typing import Any

from pydantic import Field, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from mozz_sec.data.sbc_data import TestDataSbc, ScanType
from mozz_sec.services._types import TaskStatus
from mozz_sec.services.tasks.task import BaseExecTask, BaseSubTask, TaskWithDetail


class SubSbcTask(BaseSubTask):
    """
    Represents a subtask for SBC.

    Inherits from BaseSubTask.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        file_path: The path to the file associated with the subtask.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    file_path: Path = Field(default="", alias="file", exclude=False)


class SbcCleanseData(TestDataSbc):
    """
    Represents the cleanse data for SBC.

    Inherits from TestDataSbc.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        username: The username for authentication.
        password: The password for authentication.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    username: str
    password: str


class SbcCleanseTask(TaskWithDetail):
    """
    Represents the cleanse task for SBC.

    Inherits from BaseTaskDetail.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        params: The cleanse data for SBC. It is a SbcCleanseData object.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    params: SbcCleanseData


class SbcExecTask(BaseExecTask):
    """
    Represents the execution task for SBC.

    Inherits from BaseExecTask.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        detail: The cleanse task detail for SBC. It is a SbcCleanseTask object.

    Args:
        **data: Additional keyword arguments to initialize the task.

    Returns:
        None.
    """

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
