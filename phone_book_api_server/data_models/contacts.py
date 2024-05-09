from typing import Optional

from pydantic import Field

from phone_book_api_server.data_models.base import SharedBaseModel


class ContactRequest(SharedBaseModel):
    first_name: str = Field(description="The first name of the contact")
    last_name: str = Field(description="The last name of the contact")
    phone_number: str = Field(description="The phone number of the contact")
    email_address: str = Field(description="The mail adress of the contact")


class ContactResponse(SharedBaseModel):
    first_name: str = Field(description="The first name of the contact")
    last_name: str = Field(description="The last name of the contact")
    phone_number: str = Field(description="The phone number of the contact")
    email_address: str = Field(description="The mail adress of the contact")


class UpdateContactRequest(SharedBaseModel):
    first_name: Optional[str] = Field(description="The first name of the contact")
    last_name: Optional[str] = Field(description="The last name of the contact")
    phone_number: Optional[str] = Field(description="The phone number of the contact")
    email_address: Optional[str] = Field(description="The mail adress of the contact")
