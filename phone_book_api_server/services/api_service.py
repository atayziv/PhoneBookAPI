import logging

from phone_book_api_server.clients.postgres_client import PostgresClient
from phone_book_api_server.data_models.contacts import ContactRequest


class ApiService:
    def __init__(
        self,
        postgres_client: PostgresClient,
    ) -> None:
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__postgres_client = postgres_client

    def insert_contact_data(self, contact_data: ContactRequest) -> None:
        self.__logger.info(f"Adding contact {contact_data.first_name} to the db")
        self.__postgres_client.insert_contact(contact_data)
        self.__logger.info(
            f"Successfully added a new contact with phone number : {contact_data.phone_number}"
        )
