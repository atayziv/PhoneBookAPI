from dependency_injector.wiring import inject
from fastapi import APIRouter

from phone_book_api_server.data_models.health import HealthResponse

router = APIRouter(
    prefix="",
    tags=["Health"],
)


@router.get(
    path="/health",
    response_model=HealthResponse,
)
@inject
def health() -> HealthResponse:
    return HealthResponse()
