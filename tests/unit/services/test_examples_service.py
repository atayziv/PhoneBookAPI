from unittest.mock import Mock

import pytest

from fastapi_server.data_models.example import ExampleRequest, ExampleResponse
from fastapi_server.services.examples_service import ExamplesService


@pytest.mark.parametrize(
    "example_request, expected_response",
    [
        pytest.param(
            ExampleRequest(path="file.jpg"),
            ExampleResponse(path="file.jpg", extension="jpg"),
            marks=pytest.mark.parametrize,
            id="path of a file with an extension",
        ),
        pytest.param(
            ExampleRequest(path="file"),
            ExampleResponse(path="file", extension="file"),
            marks=pytest.mark.parametrize,
            id="path of a file without an extension",
        ),
    ],
)
def test_get_extension_response(
    mock_examples_client: Mock,
    examples_service: ExamplesService,
    example_request: ExampleRequest,
    expected_response: ExampleResponse,
) -> None:
    # Arrange
    mock_examples_client.get_extension.return_value = expected_response.extension

    # Act
    extension_response = examples_service.get_extension_response(example_request)

    # Assert
    assert extension_response == expected_response

    mock_examples_client.get_extension.assert_called_once_with(example_request.path)
