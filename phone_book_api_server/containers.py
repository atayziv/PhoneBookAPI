import logging.config

from dependency_injector import containers, providers

from phone_book_api_server.clients.db_client import PostgreSQLClient
from phone_book_api_server.database.models import Contacts
from phone_book_api_server.services.contact_service import ContactService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )
    db_client = providers.Singleton(PostgreSQLClient)
    db_service = providers.Singleton(ContactService, db_client)
