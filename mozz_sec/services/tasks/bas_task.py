from __future__ import annotations

from typing import Any

from pydantic import Field, ConfigDict
from pydantic.alias_generators import to_camel
from pydantic_core import Url

from mozz_sec.data.bas_data import TestDataBas
from mozz_sec.services.tasks.task import BaseExecTask, BaseSubTask, TaskWithDetail


class SubBasTask(BaseSubTask):
    """
    Represents a subtask for BAS.

    Inherits from BaseSubTask.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class BasTaskDetail(TaskWithDetail):
    """
    Represents the task detail for BAS.

    Inherits from BaseTaskDetail.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        bas_vm_policy_url: The URL for the BAS VM policy.
        bas_container_policy_url: The URL for the BAS container policy.
        params: The test data for BAS. It is a TestDataBas object.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    bas_vm_policy_url: Url
    bas_container_policy_url: Url
    params: TestDataBas = Field(default_factory=TestDataBas, exclude=False)


class BasCleanseTask(TaskWithDetail):
    """
    Represents the cleanse task for BAS.

    Inherits from BaseTaskDetail.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        bas_vm_policy_url: The URL for the BAS VM policy.
        bas_container_policy_url: The URL for the BAS container policy.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    bas_vm_policy_url: Url
    bas_container_policy_url: Url


class BasExecTask(BaseExecTask):
    """
    Represents the execution task for BAS.

    Inherits from BaseExecTask.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        detail: The task detail for BAS. It is a BasTaskDetail object.

    Args:
        **data: Additional keyword arguments to initialize the task.

    Returns:
        None.
    """

    def __init__(self, **data: Any):
        """
        Initializes a new instance of BasExecTask.

        Args:
            **data: Additional keyword arguments to initialize the task.

        Returns:
            None.
        """
        super().__init__(**data)
        self.task_type = "BAS_EXEC"

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    detail: BasTaskDetail = Field(default_factory=BasTaskDetail)

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.task_type = "BAS_EXEC"


class BasExecTaskOut(BasExecTask):
    """
    Represents the output task for BAS execution.

    Inherits from BasExecTask.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        detail: The cleanse task detail for BAS. It is a BasCleanseTask object.
    """

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
