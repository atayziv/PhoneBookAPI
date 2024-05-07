import pytest

from fastapi_server.clients.examples_client import ExamplesClient


@pytest.mark.parametrize(
    "path, expected_extension",
    [
        pytest.param(
            "file.jpg",
            "jpg",
            marks=pytest.mark.parametrize,
            id="path of a file with an extension",
        ),
        pytest.param(
            "file",
            "file",
            marks=pytest.mark.parametrize,
            id="path of a file without an extension",
        ),
    ],
)
def test_get_extension(examples_client: ExamplesClient, path: str, expected_extension: str) -> None:
    # Act
    extension = examples_client.get_extension(path)

    # Assert
    assert extension == expected_extension
