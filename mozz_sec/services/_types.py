from __future__ import annotations

from enum import Enum

from pydantic import BeforeValidator, HttpUrl, TypeAdapter
from typing_extensions import Annotated


class TaskStatus(Enum):
    """
    Represents the status of a task.

    Attributes:
        Waiting: The task is waiting to be executed.
        Running: The task is currently running.
        Finished: The task has finished successfully.
        Fault: The task encountered an error during execution.
        Stop: The task has been stopped manually.
    """

    Waiting: str = "W"
    Running: str = "B"
    Finished: str = "R"
    Fault: str = "F"
    Stop: str = "S"


Url = Annotated[str, BeforeValidator(lambda value: str(TypeAdapter(HttpUrl).validate_python(value)))]


if __name__ == "__main__":
    print("Hello")
