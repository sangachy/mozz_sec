from __future__ import annotations

from typing import List, Any

from loguru import logger
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from mozz_sec.services._types import TaskStatus, Url
from mozz_sec.data.common_data import InstanceInfo, Common


class TaskWithProgress(BaseModel):
    """
    Represents the progress of a task.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        progress: The progress of the task as a percentage (0-100).
        status: The status of the task. It is a TaskStatus object.
        message: The message associated with the task.
        task_id: The ID of the task.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    progress: int = Field(0, ge=0, le=100)
    status: TaskStatus = TaskStatus.Waiting
    message: str = ""
    task_id: str = ""


class BaseTask(TaskWithProgress):
    """
    Represents a base task.

    Inherits from TaskProgress.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        common: The common data associated with the task. It is a Common object.
        task_type: The type of the task.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    common: Common = Field(default_factory=Common, exclude=True)
    task_type: str = Field(default="UNDEFINED", exclude=True)


class TaskWithDetail(BaseTask):
    """
    Represents the detail of a base task.

    Inherits from BaseTask.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        secguard_workspace_url: The URL for the SecGuard workspace.
        details: A list of details associated with the task.
        params: The parameters for the task.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    secguard_workspace_url: Url = "https://www.huawei.com/"
    details: List[Any] = Field(default_factory=list)
    params: Any

    def update_progress(self):
        if len(self.details) == 0:
            return
        progress = 0
        for detail in self.details:
            self.progress += detail.progress
        self.progress = int(self.progress / len(self.details))

    def update_status(self):
        logger.error("TODO")

    def start_cleanse(self):
        logger.error("开始清洗: TODO")


class BaseExecTask(BaseTask):
    """
    Represents the execution task.

    Inherits from BaseTask.

    Attributes:
        detail: The detail of the task. It is a BaseTaskDetail object.
    """

    detail: TaskWithDetail = Field(default_factory=TaskWithDetail)

    def update_progress(self):
        self.detail.update_progress()
        self.progress = self.detail.progress

    def update_status(self):
        self.detail.update_status()
        self.status = self.detail.status

    def update(self):
        pass


class BaseSubTask(TaskWithProgress):
    """
    Represents a base subtask.

    Inherits from TaskProgress.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        category: The category of the subtask.
        category_url: The URL for the category of the subtask.
        sub_category: The subcategory of the subtask.
        sub_category_url: The URL for the subcategory of the subtask.
        cover: A boolean indicating whether the subtask has a cover.
        remark: The remark for the subtask.
        report_url: The URL for the report of the subtask.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    category: str = ""
    category_url: Url = "https://www.huawei.com"
    sub_category: str = ""
    sub_category_url: Url = "https://www.huawei.com"
    cover: bool = True
    remark: str = ""
    report_url: Url = "https://www.huawei.com"


if __name__ == "__main__":
    service = BaseExecTask(
        common=Common(
            pbi="25922505",
            instance_info=InstanceInfo(instance_id="123", task_id="456"),
        )
    )
    print(service.model_dump_json(by_alias=True, indent=4))
