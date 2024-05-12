from pydantic import Field

from phone_book_api_server.data_models.base import SharedBaseModel


class InfoResponse(SharedBaseModel):
    api: str = Field(description="api name")
    version: str = Field(description="api version")
