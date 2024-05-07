from phone_book_api_server.data_models.base import SharedBaseModel


class HealthResponse(SharedBaseModel):
    status: str = "OK"
