from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contacts(Base):
    __tablename__ = "contacts"

    phone_number = Column("phone_number", String, primary_key=True)
    first_name = Column("first_name", String, nullable=False)
    last_name = Column("last_name", String, nullable=False)
    email_address = Column("email_address", String, nullable=True)
