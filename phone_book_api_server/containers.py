import logging.config

from dependency_injector import containers, providers

# from phone_book_api_server.clients.postgres_client import PostgresClient
# from phone_book_api_server.clients.db_client import DbClient
# from phone_book_api_server.services.api_service import ApiService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )

    # postgres_client = providers.Singleton(
    #     DbClient,
    # )

    # api_service = providers.Singleton(
    #     ApiService,
    #     postgres_client=postgres_client,
    # )
