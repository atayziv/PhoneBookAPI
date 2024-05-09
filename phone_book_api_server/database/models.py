from database.connection import Base, engine
from sqlalchemy import Column, String


class Contacts(Base):
    __tablename__ = "contacts"

    phone_number = Column("phone_number", String, primary_key=True)
    first_name = Column("first_name", String, nullable=False)
    last_name = Column("last_name", String, nullable=False)
    email_address = Column("email_address", String, nullable=True)


Base.metadata.create_all(engine)
