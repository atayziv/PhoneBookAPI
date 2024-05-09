from typing import List

from data_models.db import DeleteContactResponse
from database.models import Contacts
from sqlalchemy.orm import Session

from phone_book_api_server.data_models.contacts import (
    ContactRequest,
    ContactResponse,
    UpdateContactRequest,
)


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
    return db_contact


def get_contacts_list(db: Session) -> List[ContactResponse]:
    contacts_list = db.query(Contacts).limit(10).all()
    return contacts_list


def get_contact(db: Session, contact_phone_number: str) -> ContactResponse:
    contact_data = db.query(Contacts).filter_by(phone_number=contact_phone_number).one()
    return contact_data
    # return ContactResult(
    #     phone_number=contact_data.phone_number,
    #     first_name=contact_data.first_name,
    #     last_name=contact_data.last_name,
    #     email_address=contact_data.email_address,
    # )


def update_contact(
    db: Session, contact_data: UpdateContactRequest, contact_phone_number: str
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
    # return ContactResponse(
    #     phone_number=updated_contact.phone_number,
    #     first_name=updated_contact.first_name,
    #     last_name=updated_contact.last_name,
    #     email_address=updated_contact.email_address,
    # )


def delete_contact(db: Session, contact_phone_number: str) -> DeleteContactResponse:
    contact = db.query(Contacts).filter_by(phone_number=contact_phone_number).all()
    if not contact:
        return DeleteContactResponse(detail="Doesnt Exist")
    db.query(Contacts).filter_by(phone_number=contact_phone_number).delete()
    db.commit()
    return DeleteContactResponse(detail="Contact Deleted")
