import json
from pathlib import Path

import pytest
from mozz_sec.data.bas_data import TestDataBas
from pydantic import ValidationError


# Happy path tests with various realistic test values

BASE_DIR = Path(__file__).parent / "data" / "bas"


@pytest.mark.parametrize(
    "task_data_file",
    [
        BASE_DIR / "valid_01.json",
        BASE_DIR / "valid_02.json",
        BASE_DIR / "valid_03.json",
        # Add more test cases as needed
    ],
    ids=["valid_01", "valid_02", "valid_03"],
)
def test_sbc_data_happy_path(task_data_file: Path):
    with task_data_file.open(encoding="utf-8") as fp:
        TestDataBas.model_validate(json.load(fp))


# Error cases
@pytest.mark.parametrize(
    "task_data_file",
    [
        BASE_DIR / "invalid_01.json",
        BASE_DIR / "invalid_02.json",
        # Add more error cases as needed
    ],
    ids=["invalid_01", "invalid_02"],
)
def test_sbc_data_error_cases(task_data_file: Path):
    # Act / Assert
    with pytest.raises(ValidationError):
        with task_data_file.open(encoding="utf-8") as fp:
            TestDataBas.model_validate(json.load(fp))
