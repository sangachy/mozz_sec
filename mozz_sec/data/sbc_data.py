import re
from typing import List

from pydantic import BaseModel, ConfigDict, Field, model_validator, HttpUrl
from pydantic.alias_generators import to_camel


class ScanType(BaseModel):
    """
    Represents a scan type for a tasks.

    Args:
        opensource (bool, optional): Indicates if the scan includes open source analysis. Defaults to False.
        binscope (bool, optional): Indicates if the scan includes binary scope analysis. Defaults to False.
        seninfo (bool, optional): Indicates if the scan includes sensitive information analysis. Defaults to False.
        securecat (bool, optional): Indicates if the scan includes secure catalog analysis. Defaults to False.

    Returns:
        None
    Examples:
            >>> scan_type = ScanType(opensource=False, binscope=False, seninfo=True, securecat=False)
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
    Represents a file black-list for Mozzarella SBC data.

    Args:
        regex (str): The regular expression pattern for matching file names.
        examples (List[str]): The list of example file names.

    Returns:
        None"""

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
    Represents SBC data for Mozzarella.

    Args:
        url_list (List[str]): The list of URLs.
        scan_type (ScanType): The scan type.
        path_whitelist (List[str], optional): The list of path whitelists. Defaults to an empty list.
        file_blacklist (List[str], optional): The list of file blacklists. Defaults to an empty list.

    Returns:
        None"""

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
