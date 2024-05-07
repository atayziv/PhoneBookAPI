from typing import Dict
from unittest.mock import Mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest_lazyfixture import lazy_fixture

from fastapi_server.api.server import app
from fastapi_server.data_models.example import ExampleResponse


@pytest.mark.parametrize(
    "request_body",
    [
        pytest.param(
            lazy_fixture("dummy_file_with_extension_example_request"),
            marks=pytest.mark.parametrize,
            id="path of a file with an extension",
        ),
        pytest.param(
            lazy_fixture("dummy_file_without_extension_example_request"),
            marks=pytest.mark.parametrize,
            id="path of a file without an extension",
        ),
    ],
)
def test_extension(
    api_client: TestClient,
    mock_examples_service: Mock,
    dummy_example_response: ExampleResponse,
    request_body: Dict[str, str],
) -> None:
    # Arrange
    mock_examples_service.get_extension_response.return_value = dummy_example_response

    # Act
    with app.extra["container"].examples_service.override(mock_examples_service):
        response = api_client.post("/examples/extension", json=request_body)

    # Assert
    assert response.status_code == status.HTTP_200_OK

    actual = ExampleResponse(**response.json())
    expected = ExampleResponse(
        path=dummy_example_response.path,
        extension=dummy_example_response.extension,
    )
    assert actual == expected

    mock_examples_service.get_extension_response.assert_called_once_with(request_body)


@pytest.mark.parametrize(
    "request_body, error, expected_status_code",
    [
        pytest.param(
            lazy_fixture("dummy_file_with_extension_example_request"),
            ValueError,
            status.HTTP_400_BAD_REQUEST,
            marks=pytest.mark.parametrize,
            id="Bad Request [400]",
        ),
        pytest.param(
            lazy_fixture("dummy_file_with_extension_example_request"),
            FileNotFoundError,
            status.HTTP_404_NOT_FOUND,
            marks=pytest.mark.parametrize,
            id="file not found [404]",
        ),
        pytest.param(
            lazy_fixture("dummy_file_with_extension_example_request"),
            Exception,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            marks=pytest.mark.parametrize,
            id="Internal Error [500]",
        ),
    ],
)
def test_extension_error(
    api_client: TestClient,
    mock_examples_service: Mock,
    request_body: Dict[str, str],
    error: Exception,
    expected_status_code: int,
) -> None:
    # Arrange
    mock_examples_service.get_extension_response.side_effect = error

    # Act
    with app.extra["container"].examples_service.override(mock_examples_service):
        response = api_client.post("/examples/extension", json=request_body)

    # Assert
    assert response.status_code == expected_status_code
