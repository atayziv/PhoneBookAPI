import re
from typing import Any, Dict, List

import phonenumbers
from data_models.db import DeleteContactResponse
from database.models import Base, Contacts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from phone_book_api_server.constants import SETTINGS
from phone_book_api_server.data_models.contacts import (
    ContactRequest,
    ContactResponse,
    UpdateContactRequest,
)
from phone_book_api_server.exceptions.contact import ContactNotFoundError


class DbService:
    """DataBase CRUD Service."""

    def __init__(self, config: Dict[str, Any]) -> None:
        engine = create_engine(SETTINGS.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(engine)

    def insert_contact(self, contact_request: ContactRequest) -> ContactResponse:
        db = self.SessionLocal()
        new_contact = Contacts(**contact_request.__dict__)
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        contact_response = ContactResponse(**contact_request.__dict__)
        if contact_request.email_address:
            contact_response.email_address = contact_request.email_address
        db.close()
        return contact_response

    def get_contacts_list(self, limit_contacts_list: int) -> List[ContactResponse]:
        db = self.SessionLocal()
        contacts_list = db.query(Contacts).limit(limit_contacts_list).all()
        db.close()
        return contacts_list

    def get_contact(self, contact_phone_number: str) -> ContactResponse:
        db = self.SessionLocal()
        contact_data = db.query(Contacts).filter_by(phone_number=contact_phone_number).one()
        contact_response = ContactResponse(**contact_data.__dict__)
        db.close()
        return contact_response

    def update_contact(
        self, contact_data_update_request: UpdateContactRequest, contact_phone_number: str
    ) -> ContactResponse:
        db = self.SessionLocal()
        contact_data = ContactResponse(**self.get_contact(contact_phone_number).__dict__)
        if contact_data:
            if self._is_valid_number(contact_data_update_request.phone_number) and self._is_changed(
                source_object=contact_data.phone_number,
                target_object=contact_data_update_request.phone_number,
            ):
                contact_data.phone_number = contact_data_update_request.phone_number
            if self._is_valid_name(contact_data_update_request.first_name) and self._is_changed(
                source_object=contact_data.first_name,
                target_object=contact_data_update_request.first_name,
            ):
                contact_data.first_name = contact_data_update_request.first_name
            if self._is_valid_name(contact_data_update_request.last_name) and self._is_changed(
                source_object=contact_data.last_name,
                target_object=contact_data_update_request.last_name,
            ):
                contact_data.last_name = contact_data_update_request.last_name
            if self._is_valid_email(contact_data_update_request.email_address) and self._is_changed(
                source_object=contact_data.email_address,
                target_object=contact_data_update_request.email_address,
            ):
                contact_data.email_address = contact_data_update_request.email_address
            db.query(Contacts).filter_by(phone_number=contact_phone_number).update(
                contact_data.__dict__
            )
            db.commit()
            updated_contact = self.get_contact(contact_data.phone_number)
            db.close()
            return updated_contact
        raise ContactNotFoundError

    def delete_contact(self, contact_phone_number: str) -> DeleteContactResponse:
        db = self.SessionLocal()
        contact = db.query(Contacts).filter_by(phone_number=contact_phone_number).all()
        if not contact:
            return DeleteContactResponse(
                detail=f"The Contact with phone number {contact_phone_number} doesn't exist"
            )
        db.query(Contacts).filter_by(phone_number=contact_phone_number).delete()
        db.commit()
        db.close()
        return DeleteContactResponse(
            detail=f"Contact with phone number {contact_phone_number} has been successfully deleted."
        )

    def _is_changed(self, source_object: str, target_object: str) -> bool:
        if target_object:
            return bool(source_object != target_object)

    def _is_valid_number(self, phone_number: str) -> bool:
        parsed_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(parsed_number)

    def _is_valid_email(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def _is_valid_name(self, name: str) -> bool:
        return bool(name.isalpha)
