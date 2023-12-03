from enum import Enum
from typing import List, Dict

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class PluginInfoType(Enum):
    vm: str = "VM"
    container: str = "Container"


class PluginInfoParam(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    plugin_set_names: List[str] = Field(default=..., min_items=1)
    plugin_name_blacklist: List[str] = Field(default_factory=list)
    plugin_name_whitelist: List[str] = Field(default_factory=list)


class ContainerInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    grep: str
    path: str


class PluginInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    type: PluginInfoType
    params: PluginInfoParam


class TestDataBas(PluginInfoParam):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    config: Dict[str, Dict]
    container_info: Dict[str, ContainerInfo]

    plugin_extra: List[PluginInfo] = Field(default_factory=list)
    plugin_extra_tc: Dict[str, List[PluginInfo]] = Field(default_factory=dict)
