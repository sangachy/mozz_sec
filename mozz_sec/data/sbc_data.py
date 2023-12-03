import re
from typing import List

from pydantic import BaseModel, ConfigDict, Field, model_validator, HttpUrl
from pydantic.alias_generators import to_camel


class ScanType(BaseModel):
    """
    Represents the scan type.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - json_schema_extra: An optional JSON schema example for the configuration.
            - alias_generator: A function used to generate aliases for the configuration.
        opensource: A boolean indicating whether to perform opensource scanning.
        binscope: A boolean indicating whether to perform binscope scanning.
        seninfo: A boolean indicating whether to perform seninfo scanning.
        securecat: A boolean indicating whether to perform securecat scanning.

    Raises:
        ValueError: If all scan types are set to False.

    Returns:
        ScanType: The updated ScanType object.
    """
    

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": [
                {
                    "opensource": False,
                    "binscope": False,
                    "seninfo": False,
                    "securecat": False,
                }
            ]
        },
        alias_generator=to_camel,
    )

    opensource: bool = False
    binscope: bool = False
    seninfo: bool = False
    securecat: bool = False

    @model_validator(mode="after")
    def check_examples_match(self) -> "ScanType":
        if not self.opensource and not self.binscope and not self.seninfo and not self.securecat:
            raise ValueError("扫描类型全为否，无需扫描，请重新设置测试数据")
        return self


class FileBlackList(BaseModel):
    """
    Represents the file blacklist.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - json_schema_extra: An optional JSON schema example for the configuration.
            - alias_generator: A function used to generate aliases for the configuration.
        regex: The regular expression pattern for matching file names.
        examples: A list of example file names.

    Raises:
        ValueError: If the regular expression pattern does not match any of the example file names.

    Returns:
        FileBlackList: The updated FileBlackList object.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={"example": [{"regex": "^xxx$", "examples": ["XXX"]}]},
        alias_generator=to_camel,
    )

    regex: str
    examples: List[str]

    @model_validator(mode="after")
    def check_examples_match(self) -> "FileBlackList":
        regex = self.regex
        examples = self.examples

        for example in examples:
            if not re.match(regex, example):
                raise ValueError(f"正则{regex} 无法匹配示例中的{example}，请检查确保正则可以正确匹配到黑名单")
        return self


class TestDataSbc(BaseModel):
    """
    Represents the test data for SBC.

    Attributes:
        model_config: The configuration for the model. It is a ConfigDict object with the following properties:
            - populate_by_name: A boolean indicating whether to populate the configuration by name.
            - json_schema_extra: An optional JSON schema example for the configuration.
            - alias_generator: A function used to generate aliases for the configuration.
        url_list: A list of HTTP URLs.
        scan_type: The scan type. It is a ScanType object.
        path_whitelist: A list of whitelisted paths.
        file_blacklist: A list of blacklisted file names.
        rerun: A boolean indicating whether to rerun the test.

    Returns:
        TestDataSbc: The updated TestDataSbc object.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": [
                {
                    "url-list": ["https://cmc-szv.clouddrago.com"],
                    "scan-type": {
                        "opensource": False,
                        "binscope": False,
                        "seninfo": False,
                        "securecat": False,
                    },
                    "path-whitelist": [],
                    "file-blacklist": [],
                }
            ]
        },
        alias_generator=to_camel,
    )

    url_list: List[HttpUrl] = Field(default_factory=list, alias="url-list", exclude=True)
    scan_type: ScanType = Field(default=..., alias="scan-type", exclude=False)
    path_whitelist: List[str] = Field(default_factory=list, alias="path-whitelist", exclude=True)
    file_blacklist: List[str] = Field(default_factory=list, alias="file-blacklist", exclude=True)
    # 隐藏参数，暂不对外呈现
    rerun: bool = Field(default=False, exclude=True)


if __name__ == "__main__":
    file_blacklists = FileBlackList(regex="^UEG.*json$", examples=["UEG 24.0.0.json"])
    scan_type = ScanType(binscope=True)

    data = {
        "url-list": ["https://cmc-szv.clouddrago.com"],
        "scan-type": {
            "opensource": False,
            "binscope": False,
            "seninfo": True,
            "securecat": False,
        },
        "path-whitelist": [],
        "file-blacklist": [],
    }

    print(TestDataSbc.model_validate(data).model_dump_json(indent=4, by_alias=True))
