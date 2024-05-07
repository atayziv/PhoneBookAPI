from unittest.mock import Mock

import pytest

from fastapi_server.clients.examples_client import ExamplesClient
from fastapi_server.data_models.example import ExampleResponse
from fastapi_server.services.examples_service import ExamplesService


@pytest.fixture()
def mock_examples_client() -> Mock:
    return Mock(spec=ExamplesClient)


@pytest.fixture()
def examples_service(mock_examples_client: ExamplesClient) -> ExamplesService:
    return ExamplesService(mock_examples_client)


@pytest.fixture()
def dummy_expected_response() -> ExampleResponse:
    return ExampleResponse(path="file.txt", extension="txt")
