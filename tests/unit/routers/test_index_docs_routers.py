from fastapi import status
from fastapi.testclient import TestClient

from fastapi_server.constants import SETTINGS


def test_index(api_client: TestClient) -> None:
    # Act
    response = api_client.get("/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    actual = response.json()
    assert actual["api"] == SETTINGS.NAME
    assert actual["version"] == SETTINGS.VERSION


def test_docs(api_client: TestClient) -> None:
    # Act
    response = api_client.get("/docs")

    # Assert
    assert response.status_code == status.HTTP_200_OK


def test_redoc(api_client: TestClient) -> None:
    # Act
    response = api_client.get("/redoc")

    # Assert
    assert response.status_code == status.HTTP_200_OK


def test_exception_handler(api_client: TestClient) -> None:
    # Act
    response = api_client.get("/test_error")

    # Assert
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
