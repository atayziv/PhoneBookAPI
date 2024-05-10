from typing import List

from data_models.db import DeleteContactResponse
from database.models import Contacts
from sqlalchemy.orm import Session

from phone_book_api_server.data_models.contacts import (
    ContactRequest,
    ContactResponse,
    UpdateContactRequest,
)


class DbService:
    """DataBase CRUD Service."""

    def create_contact(db: Session, contact: ContactRequest) -> ContactResponse:
        db_contact = Contacts(
            phone_number=contact.phone_number,
            first_name=contact.first_name,
            last_name=contact.last_name,
            email_address=contact.email_address,
        )
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        contact_response = ContactResponse(
            phone_number=contact.phone_number,
            first_name=contact.first_name,
            last_name=contact.last_name,
        )
        if contact.email_address:
            contact_response.email_address = contact.email_address
        return contact_response

    def get_contacts_list(self, db: Session) -> List[ContactResponse]:
        contacts_list = db.query(Contacts).limit(10).all()
        return contacts_list

    def get_contact(self, db: Session, contact_phone_number: str) -> ContactResponse:
        contact_data = db.query(Contacts).filter_by(phone_number=contact_phone_number).one()
        contact_response = ContactResponse(
            phone_number=contact_data.phone_number,
            first_name=contact_data.first_name,
            last_name=contact_data.last_name,
        )
        if contact_data.email_address:
            contact_response.email_address = contact_data.email_address
        return contact_data

    def update_contact(
        self, db: Session, contact_data: UpdateContactRequest, contact_phone_number: str
    ) -> ContactResponse:
        update_query = {}
        if contact_data.phone_number:
            update_query[Contacts.phone_number] = contact_data.phone_number
        if contact_data.first_name:
            update_query[Contacts.first_name] = contact_data.first_name
        if contact_data.last_name:
            update_query[Contacts.last_name] = contact_data.last_name
        if contact_data.email_address:
            update_query[Contacts.email_address] = contact_data.email_address

        db.query(Contacts).filter_by(phone_number=contact_phone_number).update(update_query)
        db.commit()

        updated_contact = db.query(Contacts).filter_by(phone_number=contact_phone_number).one()
        return updated_contact

    def delete_contact(self, db: Session, contact_phone_number: str) -> DeleteContactResponse:
        contact = db.query(Contacts).filter_by(phone_number=contact_phone_number).all()
        if not contact:
            return DeleteContactResponse(detail="Doesnt Exist")
        db.query(Contacts).filter_by(phone_number=contact_phone_number).delete()
        db.commit()
        return DeleteContactResponse(detail="Contact Deleted")
