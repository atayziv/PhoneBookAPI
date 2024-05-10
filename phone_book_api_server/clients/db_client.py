"""PostgreSQL client."""

import logging
from typing import List

from database.models import Base, Contacts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from phone_book_api_server.constants import SETTINGS
from phone_book_api_server.data_models.contacts import ContactResponse
from phone_book_api_server.exceptions.contact import ContactAlreadyExist, ContactNotFoundError


class PostgreSQLClient:
    """PostgreSQL Client Class."""

    def __init__(
        self,
    ) -> None:
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        engine = create_engine(SETTINGS.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(engine)

    def insert_contact(self, new_contact: Contacts) -> None:
        self.__logger.info("Inserting new contact into 'contacts' table in PostgreSQL.")
        db = self.SessionLocal()
        try:
            db.add(new_contact)
            db.commit()
            db.refresh(new_contact)
            self.__logger.info("Data has been successfully inserted into the 'contacts' table.")
        except:
            raise ContactAlreadyExist
        finally:
            db.close()

    def get_contacts(self, limit_contacts_list: int) -> List[ContactResponse]:
        self.__logger.info("Get a list of contacts with pagination from 'contacts' table.")
        db = self.SessionLocal()
        try:
            contacts_list = db.query(Contacts).limit(limit_contacts_list).all()
            self.__logger.info(
                "Successfully got a list of contacts with pagination from 'contacts' table."
            )
            return contacts_list
        finally:
            db.close()

    def get_contact(self, contact_phone_number: str) -> ContactResponse:
        self.__logger.info("Get contact from 'contacts' table.")
        db = self.SessionLocal()
        try:
            contact_data = db.query(Contacts).filter_by(phone_number=contact_phone_number).one()
            self.__logger.info("Successfully got contact from 'contacts' table.")
            return contact_data
        except:
            raise ContactNotFoundError
        finally:
            db.close()

    def update_contact(self, contact_phone_number: str, contact_data: ContactResponse) -> None:
        self.__logger.info("Update contact on 'contacts' table.")
        db = self.SessionLocal()
        try:
            db.query(Contacts).filter_by(phone_number=contact_phone_number).update(
                contact_data.__dict__
            )
            db.commit()
            self.__logger.info("Successfully updated contact on 'contacts' table.")
        except:
            raise ContactAlreadyExist
        finally:
            db.close()

    def delete_contact(self, contact_phone_number: str):
        self.__logger.info("Delete contact from 'contacts' table.")
        db = self.SessionLocal()
        try:
            db.query(Contacts).filter_by(phone_number=contact_phone_number).delete()
            db.commit()
            self.__logger.info("Successfully removed contact from 'contacts' table.")
        finally:
            db.close()
