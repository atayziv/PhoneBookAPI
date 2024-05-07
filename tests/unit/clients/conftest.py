import pytest

from fastapi_server.clients.examples_client import ExamplesClient


@pytest.fixture(scope="session")
def examples_client() -> ExamplesClient:
    return ExamplesClient()
