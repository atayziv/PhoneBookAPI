import re
from typing import List

import phonenumbers
from data_models.db import DeleteContactResponse
from database.models import Contacts

from phone_book_api_server.clients.db_client import PostgreSQLClient
from phone_book_api_server.data_models.contacts import (
    ContactRequest,
    ContactResponse,
    UpdateContactRequest,
)
from phone_book_api_server.exceptions.contact import (
    InvalidContactEmail,
    InvalidContactName,
    InvalidContactNumber,
)


class DbService:
    """DataBase CRUD Service."""

    def __init__(self, db_client: PostgreSQLClient) -> None:
        self.__db_client = db_client

    def insert_contact(self, contact_request: ContactRequest) -> ContactResponse:
        new_contact = Contacts(**contact_request.__dict__)
        if (
            self._is_valid_number(new_contact.phone_number)
            and self._is_valid_email(new_contact.email_address)
            and self._is_valid_name(new_contact.first_name)
            and self._is_valid_name(new_contact.last_name)
        ):
            self.__db_client.insert_contact(new_contact)
            contact_response = self.get_contact(contact_request.phone_number)
            return contact_response

    def get_contacts_list(self, limit_contacts_list: int) -> List[ContactResponse]:
        contacts_list = self.__db_client.get_contacts(limit_contacts_list)
        return contacts_list

    def get_contact(self, contact_phone_number: str) -> ContactResponse:
        if self._is_valid_number(contact_phone_number):
            contact_data = self.__db_client.get_contact(contact_phone_number)
            contact_response = ContactResponse(**contact_data.__dict__)
            return contact_response
        raise InvalidContactNumber(detail="Invalid phone number.")

    def update_contact(
        self, contact_data_update_request: UpdateContactRequest, contact_phone_number: str
    ) -> ContactResponse:
        contact_data = ContactResponse(**self.get_contact(contact_phone_number).__dict__)
        if contact_data_update_request.phone_number and self._is_valid_number(
            contact_data_update_request.phone_number
        ):
            contact_data.phone_number = contact_data_update_request.phone_number
        elif contact_data_update_request.first_name and self._is_valid_name(
            contact_data_update_request.first_name
        ):
            contact_data.first_name = contact_data_update_request.first_name
        elif contact_data_update_request.last_name and self._is_valid_name(
            contact_data_update_request.last_name
        ):
            contact_data.last_name = contact_data_update_request.last_name
        elif contact_data_update_request.email_address and self._is_valid_email(
            contact_data_update_request.email_address
        ):
            contact_data.email_address = contact_data_update_request.email_address
        self.__db_client.update_contact(contact_phone_number, contact_data)
        updated_contact = self.get_contact(contact_data.phone_number)
        return updated_contact

    def delete_contact(self, contact_phone_number: str) -> DeleteContactResponse:
        if self._is_valid_number(contact_phone_number):
            contact = self.get_contact(contact_phone_number)
            if not contact:
                return DeleteContactResponse(
                    detail=f"The Contact with phone number {contact_phone_number} doesn't exist"
                )
            self.__db_client.delete_contact(contact_phone_number)
            return DeleteContactResponse(
                detail=f"Contact with phone number {contact_phone_number} has been successfully deleted."
            )
        raise InvalidContactNumber(detail=f"Invalid contact phone number.")

    def _is_valid_number(self, phone_number: str) -> bool:
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed_number):
                return True
        except:
            raise InvalidContactNumber(detail="Invalid phone number.")

    def _is_valid_email(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            raise InvalidContactEmail(detail="Invalid contact email address.")
        return True

    def _is_valid_name(self, name: str) -> bool:
        if not name.isalpha():
            raise InvalidContactName(detail="Invalid contact name.")
        return True
