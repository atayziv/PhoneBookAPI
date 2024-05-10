import logging.config

from dependency_injector import containers, providers

# from phone_book_api_server.database.models import Contacts
from phone_book_api_server.services.db_service import DbService

# from phone_book_api_server.database.connection import get_db


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )

    db_service = providers.Singleton(DbService)
