import pytest

from phone_book_api_server.clients.db_client import PostgreSQLClient
from phone_book_api_server.data_models.contacts import ContactResponse
from phone_book_api_server.database.models import Contacts


@pytest.fixture()
def db_client() -> PostgreSQLClient:
    """Contact Service fixture."""
    return PostgreSQLClient()


@pytest.fixture()
def dummy_phone_number() -> str:
    """Expected Status Code."""
    return "+972546685213"


@pytest.fixture()
def dummy_contact_insert_request() -> Contacts:
    """Dummy Contact For DB Insertion."""
    return Contacts(
        phone_number="+97252664887",
        first_name="dummyname",
        last_name="dummyname",
        email_address="dummy@mail.com",
    )


@pytest.fixture()
def dummy_limit_pagination_feature() -> int:
    """Dummy Limit Pagination Feature."""
    return 10


@pytest.fixture()
def update_contact_data_response() -> ContactResponse:
    return ContactResponse(
        phone_number="+972546643567",
        first_name="dummyname",
        last_name="dummyname",
        email_address="dummy@dummy.com",
    )
