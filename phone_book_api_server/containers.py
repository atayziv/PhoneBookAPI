import logging.config

from dependency_injector import containers, providers

from phone_book_api_server.clients.db_client import PostgreSQLClient
from phone_book_api_server.services.db_service import DbService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )
    db_client = providers.Singleton(PostgreSQLClient)
    db_service = providers.Singleton(DbService, db_client)
