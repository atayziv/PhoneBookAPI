from phone_book_api_server.data_models.base import SharedBaseModel


class DeleteContactResponse(SharedBaseModel):
    detail: str
