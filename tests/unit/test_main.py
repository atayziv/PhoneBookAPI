from pytest_mock import MockerFixture

from fastapi_server import __main__


def test_init(mocker: MockerFixture) -> None:
    mocker.patch.object(__main__, "__name__", "__main__")
    mock_uvicorn = mocker.patch("uvicorn.run", return_value=None)
    __main__.init()
    mock_uvicorn.assert_called_once()
