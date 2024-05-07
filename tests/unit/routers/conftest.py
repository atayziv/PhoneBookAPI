from typing import Dict
from unittest.mock import Mock

import pytest
from fastapi import Request, Response
from fastapi.testclient import TestClient

from fastapi_server.api.server import app
from fastapi_server.data_models.example import ExampleResponse
from fastapi_server.services.examples_service import ExamplesService


@pytest.fixture(scope="session")
def api_client() -> TestClient:
    async def test_error(_: Request) -> Response:
        raise Exception("Test Error")  # pylint: disable=broad-exception-raised

    app.add_api_route("/test_error", test_error)

    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture()
def mock_examples_service() -> Mock:
    return Mock(spec=ExamplesService)


@pytest.fixture(scope="session")
def dummy_file_with_extension_example_request() -> Dict[str, str]:
    return {"path": "file.jpg"}


@pytest.fixture(scope="session")
def dummy_file_without_extension_example_request() -> Dict[str, str]:
    return {"path": "file"}


@pytest.fixture(scope="session")
def dummy_example_response() -> ExampleResponse:
    return ExampleResponse(
        path="mocked_path",
        extension="mocked_name",
    )
