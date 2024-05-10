from typing import Optional

from pydantic import Field

from phone_book_api_server.data_models.base import SharedBaseModel


class ContactRequest(SharedBaseModel):
    first_name: str = Field(description="The first name of the contact")
    last_name: str = Field(description="The last name of the contact")
    phone_number: str = Field(description="The phone number of the contact")
    email_address: Optional[str] = Field(description="The mail adress of the contact")

    class Config:
        orm_mode = True


class ContactResponse(SharedBaseModel):
    first_name: str = Field(description="The first name of the contact")
    last_name: str = Field(description="The last name of the contact")
    phone_number: str = Field(description="The phone number of the contact")
    email_address: Optional[str] = Field(description="The mail adress of the contact")

    class Config:
        orm_mode = True


# class ContactResult(SharedBaseModel):
#     first_name: str = Field(description="The first name of the contact")
#     last_name: str = Field(description="The last name of the contact")
#     phone_number: str = Field(description="The phone number of the contact")
#     email_address: Optional[str] = Field(description="The mail adress of the contact")

#     def to_response(self) -> ContactResponse:
#         contact_response = ContactResponse(
#             first_name=self.first_name, last_name=self.last_name, phone_number=self.phone_number
#         )
#         if self.email_address:
#             contact_response.email_address = self.email_address
#         return contact_response


class UpdateContactRequest(SharedBaseModel):
    first_name: Optional[str] = Field(description="The first name of the contact")
    last_name: Optional[str] = Field(description="The last name of the contact")
    phone_number: Optional[str] = Field(description="The phone number of the contact")
    email_address: Optional[str] = Field(description="The mail adress of the contact")
