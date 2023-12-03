from __future__ import annotations

from enum import Enum

from pydantic import BeforeValidator, HttpUrl, TypeAdapter
from typing_extensions import Annotated


class TaskStatus(Enum):
    Waiting: str = "W"
    Running: str = "B"
    Finished: str = "R"
    Fault: str = "F"
    Stop: str = "S"


Url = Annotated[str, BeforeValidator(lambda value: str(TypeAdapter(HttpUrl).validate_python(value)))]


if __name__ == "__main__":
    print("Hello")
