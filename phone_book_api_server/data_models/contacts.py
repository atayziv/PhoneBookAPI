from pydantic import Field

from phone_book_api_server.data_models.base import SharedBaseModel


class ContactResponse(SharedBaseModel):
    first_name: str = Field(description="name")
    last_name: str = Field(description="last_name")
    phone_number: str = Field(description="phone_number")
    adress: str = Field(description="adress")
