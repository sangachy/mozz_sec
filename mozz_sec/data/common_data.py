from __future__ import annotations

from typing import Union, List

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class InstanceInfo(BaseModel):
    """
    Represents information about an instance.

    Args:
        instance_id (str): The ID of the instance.
        task_id (str): The ID of the tasks associated with the instance.

    Returns:
        None

    Examples:
        >>> instance = InstanceInfo(instance_id="123", task_id="456")"""

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={"example": [{"instanceId": "123", "taskId": "456"}]},
        alias_generator=to_camel,
    )

    instance_id: str = Field(default="123", alias="instanceId")
    task_id: str = Field(default="456", alias="taskId")


class Common(BaseModel):
    """
    Represents common attributes for a services.

    Args:
        pbi (Union[str, int]): The PBI (Product Backlog Item) associated with the services.
        instance_info (InstanceInfo, optional): Information about the instance. Defaults to None.

    Returns:
        None
    Examples:
        >>> common = Common(pbi="25922505", instance_info=InstanceInfo(instance_id="123", task_id="456"))
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": [
                {
                    "pbi": "25922505",
                    "instanceInfo": {"instanceId": "123", "taskId": "456"},
                }
            ]
        },
        alias_generator=to_camel,
    )

    pbi: Union[str, int] = "0"
    instance_info: InstanceInfo = Field(default_factory=InstanceInfo, alias="instanceInfo")


class Params(BaseModel):
    """
    Represents the parameters for a model.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - json_schema_extra: An optional JSON schema example for the configuration.
            - alias_generator: A function used to generate aliases for the configuration.
    """
    
    model_config = ConfigDict(populate_by_name=True, json_schema_extra={"example": [{}]}, alias_generator=to_camel)


class EnvInfo(BaseModel):
    """
    Represents the environment information.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - json_schema_extra: An optional JSON schema example for the configuration.
            - alias_generator: A function used to generate aliases for the configuration.
        containers: A list of strings representing the available containers.
        vms: A list of strings representing the available virtual machines.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={"example": [{"containers": ["All", "sm", "cmpcc"], "vms": ["None", "OMU", "PBUC"]}]},
        alias_generator=to_camel,
    )

    containers: List[str] = Field(default_factory=list)
    vms: List[str] = Field(default_factory=list)


class CommonData(BaseModel):
    """
    Represents the common data.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - alias_generator: A function used to generate aliases for the configuration.
        common: The common data. It is a Common object.
        params: The parameters for the model. It is a Params object.
        env_info: The environment information. It is an EnvInfo object.
    """
    
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    common: Common = Field(default=..., exclude=True)
    params: Params = Field(default=..., exclude=False)
    env_info: EnvInfo = Field(default=..., alias="envInfo", exclude=True)
