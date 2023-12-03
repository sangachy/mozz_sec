import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from loguru import logger

from mozz_sec.services.apps.sbc_exec_app import app as sbc_app
from mozz_sec.services.apps.data_cleanse_app import app as cleanse_app
from mozz_sec.services.apps.bas_exec_app import app as bas_app

from mozz_sec.services.tasks.cleanse_task import AnalyseTask

client_sbc = TestClient(sbc_app)
client_bas = TestClient(bas_app)
client_cleanse = TestClient(cleanse_app)


@pytest.mark.parametrize(
    "task_id, data_path",
    [
        ("task-007", Path(__file__).parent.parent / "data" / "sbc_exec" / "task-001.json"),
    ],
)
def test_create_task_happy_path_sbc(task_id: str, data_path: Path):
    # Act
    with data_path.open(encoding="utf-8") as fp:
        data = json.load(fp)
    print(data)
    response = client_sbc.post(f"/executor/v1/tools/sbc/tasks/{task_id}", json=data)
    # Assert
    logger.info(data)
    logger.info(response.text)
    assert response.status_code == 201

    analyse_data = AnalyseTask(
        source="",
        description="",
        creator="",
        instance_id="123",
        analysts=["1"],
        pbi="0",
        strategy_task_id="",
        data=data["detail"],
    )
    data = json.loads(analyse_data.model_dump_json(by_alias=True))
    response = client_cleanse.post("/cleanse/v1/tools/sbc/tasks", json=data)
    assert response.status_code == 201


@pytest.mark.parametrize(
    "task_id, data_path",
    [
        ("task-007", Path(__file__).parent.parent / "data" / "bas_exec" / "task-001.json"),
    ],
)
def test_create_task_happy_path_bas(task_id: str, data_path: Path):
    # Act
    with data_path.open(encoding="utf-8") as fp:
        data = json.load(fp)

    response = client_bas.post(f"/executor/v1/tools/bas/tasks/{task_id}", json=data)
    # Assert
    logger.info(response.text)
    assert response.status_code == 201

    response = client_sbc.get(f"/executor/v1/tools/bas/tasks/{task_id}")
    assert response.status_code == 404

    analyse_data = AnalyseTask(
        source="",
        description="",
        creator="",
        instance_id="123",
        analysts=["1"],
        pbi="0",
        strategy_task_id="",
        data=data["detail"],
    )
    data = json.loads(analyse_data.model_dump_json(by_alias=True))
    logger.error(json.dumps(data, indent=4))
    response = client_cleanse.post("/cleanse/v1/tools/bas/tasks", json=data)
    logger.error(response.text)
    assert response.status_code == 201
