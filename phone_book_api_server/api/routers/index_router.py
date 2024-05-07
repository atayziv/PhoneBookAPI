"""Index route."""

from dependency_injector.wiring import inject
from fastapi import APIRouter
from starlette import status

from ... import SETTINGS
from ...data_models.info import InfoResponse

router = APIRouter(
    prefix="",
    tags=["Index"],
    responses={
        status.HTTP_200_OK: {"description": "OK"},
    },
)


@router.get("/", response_model=InfoResponse)
@inject
def index() -> InfoResponse:
    """Server Info."""
    return InfoResponse(api=SETTINGS.NAME, version=SETTINGS.VERSION)
