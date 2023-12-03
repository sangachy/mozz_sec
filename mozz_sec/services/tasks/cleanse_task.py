from typing import Union, List, Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from mozz_sec.services.tasks.bas_task import BasCleanseTask
from mozz_sec.services.tasks.sbc_task import SbcCleanseTask


class AnalyseTask(BaseModel):
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
