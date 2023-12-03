from enum import Enum
from typing import List, Dict

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class PluginInfoType(Enum):
    """
    Represents the plugin information type.

    Attributes:
        vm: The plugin information type is for a virtual machine.
        container: The plugin information type is for a container.
    """
    
    vm: str = "VM"
    container: str = "Container"


class PluginInfoParam(BaseModel):
    """
    Represents the plugin information parameters.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        plugin_set_names: A list of plugin set names.
        plugin_name_blacklist: A list of blacklisted plugin names.
        plugin_name_whitelist: A list of whitelisted plugin names.
    """
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    plugin_set_names: List[str] = Field(default=..., min_items=1)
    plugin_name_blacklist: List[str] = Field(default_factory=list)
    plugin_name_whitelist: List[str] = Field(default_factory=list)


class ContainerInfo(BaseModel):
    """
    Represents the container information.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        grep: The grep command to search for a pattern in the container.
        path: The path to search for the pattern in the container.
    """
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    grep: str
    path: str


class PluginInfo(BaseModel):
    """
    Represents the plugin information.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        type: The type of the plugin information. It is a PluginInfoType object.
        params: The parameters for the plugin information. It is a PluginInfoParam object.
    """
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    type: PluginInfoType
    params: PluginInfoParam


class TestDataBas(PluginInfoParam):
    """
    Represents the test data for BAS.

    Inherits from PluginInfoParam.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        config: A dictionary representing the configuration.
        container_info: A dictionary representing the container information.
        plugin_extra: A list of additional plugin information. Each item is a PluginInfo object.
        plugin_extra_tc: A dictionary mapping test cases to lists of additional plugin information. The keys are test case names and the values are lists of PluginInfo objects.
    """
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    config: Dict[str, Dict]
    container_info: Dict[str, ContainerInfo]

    plugin_extra: List[PluginInfo] = Field(default_factory=list)
    plugin_extra_tc: Dict[str, List[PluginInfo]] = Field(default_factory=dict)
