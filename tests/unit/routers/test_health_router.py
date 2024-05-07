from fastapi import status
from fastapi.testclient import TestClient

from fastapi_server.data_models.health import HealthResponse


def test_health(api_client: TestClient) -> None:
    # Act
    response = api_client.get("/health")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    actual = response.json()
    assert HealthResponse(**actual) == HealthResponse()
