from typing import Union, List, Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from mozz_sec.services.tasks.bas_task import BasCleanseTask
from mozz_sec.services.tasks.sbc_task import SbcCleanseTask


class AnalyseTask(BaseModel):
    """
    Represents an analysis task.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        source: The source of the analysis task.
        description: The description of the analysis task.
        creator: The creator of the analysis task.
        instance_id: The ID of the instance associated with the analysis task.
        analysts: A list of analysts assigned to the analysis task.
        pbi: The PBI (Product Backlog Item) associated with the analysis task.
        strategy_task_id: The ID of the strategy task associated with the analysis task.
        data: The data associated with the analysis task. It can be either a BasCleanseTask or SbcCleanseTask object.
        task_type: The type of the analysis task.
    """

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    source: str
    description: str
    creator: str
    instance_id: Union[str, int] = Field(default=..., alias="instanceId")
    analysts: List[str] = Field(default_factory=list)
    pbi: Union[str, int]
    strategy_task_id: Union[str, int] = Field(default=..., alias="strategyTaskId")
    data: Union[BasCleanseTask, SbcCleanseTask]

    task_type: str = "DATA_CLEAN"

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.pbi = f"{self.pbi}"
        self.strategy_task_id = f"{self.strategy_task_id}"
        self.instance_id = f"{self.instance_id}"
