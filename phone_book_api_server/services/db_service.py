from typing import Any, Dict, List

from data_models.db import DeleteContactResponse
from database.models import Base, Contacts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from phone_book_api_server.data_models.contacts import (
    ContactRequest,
    ContactResponse,
    UpdateContactRequest,
)


class DbService:
    """DataBase CRUD Service."""

    def __init__(self, config: Dict[str, Any]) -> None:
        engine = create_engine(config["postgres"]["connection_string"])
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(engine)

    def create_contact(self, contact: ContactRequest) -> ContactResponse:
        db = self.SessionLocal()
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
        db.close()
        return contact_response

    def get_contacts_list(self) -> List[ContactResponse]:
        db = self.SessionLocal()
        contacts_list = db.query(Contacts).limit(10).all()
        db.close()
        return contacts_list

    def get_contact(self, contact_phone_number: str) -> ContactResponse:
        db = self.SessionLocal()
        contact_data = db.query(Contacts).filter_by(phone_number=contact_phone_number).one()
        contact_response = ContactResponse(
            phone_number=contact_data.phone_number,
            first_name=contact_data.first_name,
            last_name=contact_data.last_name,
        )
        if contact_data.email_address:
            contact_response.email_address = contact_data.email_address
        db.close()
        return contact_data

    def update_contact(
        self, contact_data: UpdateContactRequest, contact_phone_number: str
    ) -> ContactResponse:
        db = self.SessionLocal()
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
        updated_contact = (
            db.query(Contacts).filter_by(phone_number=update_query[Contacts.phone_number]).one()
        )
        db.close()
        return updated_contact

    def delete_contact(self, contact_phone_number: str) -> DeleteContactResponse:
        db = self.SessionLocal()
        contact = db.query(Contacts).filter_by(phone_number=contact_phone_number).all()
        if not contact:
            return DeleteContactResponse(detail="Doesnt Exist")
        db.query(Contacts).filter_by(phone_number=contact_phone_number).delete()
        db.commit()
        db.close()
        return DeleteContactResponse(detail="Contact Deleted")
