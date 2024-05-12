from typing import Any, Dict, Generator, List
from unittest.mock import Mock

import pytest
from fastapi import Request, Response
from fastapi.testclient import TestClient

from phone_book_api_server.api.server import app
from phone_book_api_server.data_models.contacts import ContactResponse
from phone_book_api_server.data_models.db import DeleteContactResponse
from phone_book_api_server.services.contact_service import ContactService


@pytest.fixture(scope="module")
def api_client() -> Generator[TestClient, None, None]:
    """Test Client fixture."""
    client = TestClient(app)
    yield client


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
def dummy_updated_contact_data() -> ContactResponse:
    """Dummy Contact Response."""
    return ContactResponse(
        phone_number="+972546643565",
        first_name="updatedname",
        last_name="updatedname",
        email_address="update@dummy.com",
    )


@pytest.fixture()
def mock_contact_service() -> Generator[Mock, None, None]:
    """Contact Service fixture."""
    yield Mock(spec=ContactService)


@pytest.fixture()
def contact_route_create_request() -> Dict[str, str]:
    """Phone Book Api Request."""
    return {
        "firstName": "dummy",
        "lastName": "dummy",
        "phoneNumber": "+972525252525",
        "emailAddress": "dummy@dummy.com",
    }


@pytest.fixture()
def contact_route_update_request() -> Dict[str, str]:
    """Phone Book Api Request."""
    return {
        "firstName": "updatedname",
        "lastName": "updatedname",
        "phoneNumber": "+972546643565",
        "emailAddress": "update@dummy.com",
    }


@pytest.fixture()
def dummy_limit_param() -> int:
    """Dummy Limit Paramater For  Pagination Feature."""
    return 10


@pytest.fixture()
def dummy_contacts_list() -> List[ContactResponse]:
    """Dummy Contacts list."""
    dummy_contact_response = ContactResponse(
        phone_number="+972546643567",
        first_name="dummyname",
        last_name="dummyname",
        email_address="dummy@dummy.com",
    )
    return [dummy_contact_response, dummy_contact_response, dummy_contact_response]


@pytest.fixture()
def dummy_delete_contact_response() -> DeleteContactResponse:
    """Dummy Delete Contact Response."""
    return DeleteContactResponse(
        detail=f"Contact with phone number +972546643567 has been successfully deleted."
    )


# @pytest.fixture()
# def mock_examples_service() -> Mock:
#     return Mock(spec=ExamplesService)


# @pytest.fixture(scope="session")
# def dummy_file_with_extension_example_request() -> Dict[str, str]:
#     return {"path": "file.jpg"}


# @pytest.fixture(scope="session")
# def dummy_file_without_extension_example_request() -> Dict[str, str]:
#     return {"path": "file"}


# @pytest.fixture(scope="session")
# def dummy_example_response() -> ExampleResponse:
#     return ExampleResponse(
#         path="mocked_path",
#         extension="mocked_name",
#     )
