import json

import pytest
from fastapi.testclient import TestClient
from mozz_sec.services.apps.sbc_exec_app import app, TASK_LIST
from mozz_sec.services.tasks.sbc_task import SbcExecTask

client = TestClient(app)


# Define a fixture for the task data
@pytest.fixture
def task_data():
    data = {
        "detail": {
            "params": {
                "username": "p_mozzps",
                "password": "Huawei12#$",
                "url-list": [],
                "scan-type": {"binscope": True},
            }
        }
    }
    return json.loads(SbcExecTask.model_validate(data).model_dump_json(by_alias=True))


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "task_id, expected_status",
    [
        ("task-001", 201),  # ID: HP-1
        ("task-002", 201),  # ID: HP-2
        ("task-003", 201),  # ID: HP-3
    ],
)
def test_create_task_happy_path(task_id, expected_status, task_data):
    # Act
    response = client.post(f"/executor/v1/tools/sbc/tasks/{task_id}", json=task_data)

    task_data["taskId"] = task_id
    # Assert
    assert response.status_code == expected_status
    assert response.json() == task_data
    assert task_id in TASK_LIST
    assert TASK_LIST[task_id] == SbcExecTask.model_validate(task_data)


# Edge cases
@pytest.mark.parametrize(
    "task_id, expected_status",
    [
        ("", 404),  # ID: EC-1: Empty task_id
        ("task-004", 422),  # ID: EC-2: None task_data
    ],
)
def test_create_task_edge_cases(task_id, expected_status, task_data):
    # Act
    response = client.post(f"/executor/v1/tools/sbc/tasks/{task_id}", json=None if task_id else task_data)
    # Assert
    assert response.status_code == expected_status


# Error cases
@pytest.mark.parametrize(
    "task_id, expected_status",
    [
        ("task-001", 409),  # ID: ERR-1: Duplicate task_id
    ],
)
def test_create_task_error_cases(task_id, expected_status, task_data):
    # Arrange
    TASK_LIST[task_id] = SbcExecTask.model_validate(task_data)  # Simulate existing task
    # Act
    response = client.post(f"/executor/v1/tools/sbc/tasks/{task_id}", json=task_data)

    # Assert
    assert response.status_code == expected_status
    assert response.json()["detail"] == f"Task with task_id {task_id} already exists."
