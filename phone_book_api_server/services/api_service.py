import logging

from phone_book_api_server.clients.postgres_client import ExamplesClient
from phone_book_api_server.data_models.contacts import ContractData, ExampleRequest


class ApiService:
    def __init__(
        self,
        examples_client: ExamplesClient,
    ) -> None:
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.__examples_client = examples_client

    def insert_contract_data(self, example_request: ExampleRequest) -> ContractData:
        self.__logger.debug("Add a new contract")
        result = self.__examples_client.get_extension(example_request.path)
        contract_data = ContractData(
            first_name=first_name, last_name=last_name, phone_number=phone_number, adress=adress
        )
