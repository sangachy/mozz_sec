from __future__ import annotations

from typing import List, Any

from loguru import logger
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from mozz_sec.services._types import TaskStatus, Url
from mozz_sec.data.common_data import InstanceInfo, Common


class TaskProgress(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    progress: int = Field(0, ge=0, le=100)
    status: TaskStatus = TaskStatus.Waiting
    message: str = ""
    task_id: str = ""


class BaseTask(TaskProgress):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    common: Common = Field(default_factory=Common, exclude=True)
    task_type: str = Field(default="UNDEFINED", exclude=True)


class BaseTaskDetail(BaseTask):
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
    detail: BaseTaskDetail = Field(default_factory=BaseTaskDetail)

    def update_progress(self):
        self.detail.update_progress()
        self.progress = self.detail.progress

    def update_status(self):
        self.detail.update_status()
        self.status = self.detail.status

    def update(self):
        pass


class BaseSubTask(TaskProgress):
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
