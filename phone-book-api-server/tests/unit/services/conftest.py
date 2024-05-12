from typing import List
from unittest.mock import Mock

import pytest

from phone_book_api_server.clients.db_client import PostgreSQLClient
from phone_book_api_server.data_models.contacts import ContactResponse
from phone_book_api_server.data_models.db import DeleteContactResponse
from phone_book_api_server.exceptions.contact import (
    InvalidContactEmail,
    InvalidContactName,
    InvalidContactNumber,
)
from phone_book_api_server.services.contact_service import ContactService


@pytest.fixture()
def dummy_contact_data() -> ContactResponse:
    """Dummy Contact Response."""
    return ContactResponse(
        phone_number="+972546643567",
        first_name="dummyname",
        last_name="dummyname",
        email_address="dummy@dummy.com",
    )


@pytest.fixture()
def dummy_contact_data_without_email() -> ContactResponse:
    """Dummy Contact Response Without Email Address."""
    return ContactResponse(
        phone_number="+972546643567",
        first_name="dummyname",
        last_name="dummyname",
    )


@pytest.fixture(scope="function")
def dummy_contact_invalid_number() -> ContactResponse:
    """Dummy Contact Response With Invalid Phone Number."""
    return ContactResponse(
        phone_number="0546643567",
        first_name="dummyname",
        last_name="dummyname",
        email_address="dummy@dummy.com",
    )


@pytest.fixture(scope="function")
def dummy_contact_invalid_email() -> ContactResponse:
    """Dummy Contact Response With Invalid Email Address."""
    return ContactResponse(
        phone_number="+972546643567",
        first_name="dummyname",
        last_name="dummyname",
        email_address="dummydummy.com",
    )


@pytest.fixture()
def dummy_contact_invalid_name(scope="function") -> ContactResponse:
    """Dummy Contact Response With Invalid Email Address."""
    return ContactResponse(
        phone_number="+972546643567",
        first_name="dummy!name",
        last_name="dummyname",
        email_address="dummy@dummy.com",
    )


@pytest.fixture()
def dummy_contacts_list() -> List[ContactResponse]:
    """Dummy Contacts list."""
    return [dummy_contact_data, dummy_contact_data, dummy_contact_data]


@pytest.fixture()
def mock_db_client() -> Mock:
    return Mock(spec=PostgreSQLClient)


@pytest.fixture()
def contact_service(mock_db_client: Mock) -> ContactService:
    """Contact Service fixture."""
    return ContactService(db_client=mock_db_client)


@pytest.fixture()
def limit_list_size_response() -> int:
    """Limit Pagination For Contacts List Response."""
    return 10


@pytest.fixture()
def dummy_phone_number() -> str:
    """Dummy Phone Number."""
    return "+972546643567"


@pytest.fixture(scope="function")
def invalid_contact_number_exception() -> InvalidContactNumber:
    """Dummy Invalid Contact Number Exception."""
    return InvalidContactNumber


@pytest.fixture(scope="function")
def invalid_contact_email_exception() -> InvalidContactEmail:
    """Dummy Invalid Contact Email Exception."""
    return InvalidContactEmail


@pytest.fixture(scope="function")
def invalid_contact_name_exception() -> InvalidContactName:
    """Dummy Invalid Contact Name Exception."""
    return InvalidContactName


@pytest.fixture()
def delete_contact_response_successfuly() -> DeleteContactResponse:
    """Dummy Delete Contact Resppnse."""
    return DeleteContactResponse(
        detail="Contact with phone number +972546643567 has been successfully deleted."
    )
