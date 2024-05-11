"""Phone Book API Router Unit Tests."""

from typing import Dict, List
from unittest.mock import Mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from phone_book_api_server.api.server import app
from phone_book_api_server.data_models.contacts import ContactResponse
from phone_book_api_server.data_models.db import DeleteContactResponse
from phone_book_api_server.exceptions.contact import (
    ContactAlreadyExist,
    ContactNotFoundError,
    InvalidContactParams,
)
from phone_book_api_server.services.contact_service import ContactService


def test_create_contact_router(
    api_client: TestClient,
    dummy_contact_data: ContactResponse,
    mock_contact_service: ContactService,
    contact_route_create_request: Dict[str, str],
) -> None:
    # Arrange
    mock_contact_service.insert_contact.return_value = dummy_contact_data

    # Act
    with app.extra["container"].contact_service.override(mock_contact_service):
        response = api_client.post("/contacts", json=contact_route_create_request)
    # Assert
    assert response.status_code == 200


@pytest.mark.parametrize(
    "error, expected_status_code",
    [
        pytest.param(
            InvalidContactParams,
            status.HTTP_400_BAD_REQUEST,
            marks=pytest.mark.parametrize,
            id="Bad Request [400]",
        ),
        pytest.param(
            ContactAlreadyExist,
            status.HTTP_409_CONFLICT,
            marks=pytest.mark.parametrize,
            id="Conflict[409]",
        ),
        pytest.param(
            Exception,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            marks=pytest.mark.parametrize,
            id="Internal Error [500]",
        ),
    ],
)
def test_create_contact_route_error(
    api_client: TestClient,
    mock_contact_service: ContactService,
    contact_route_create_request: Dict[str, str],
    error: Exception,
    expected_status_code: int,
):
    # Arrange
    mock_contact_service.insert_contact.side_effect = error

    # Act
    with app.extra["container"].contact_service.override(mock_contact_service):
        response = api_client.post("/contacts", json=contact_route_create_request)

    # Assert
    assert response.status_code == expected_status_code


def test_get_contact_router(
    api_client: TestClient,
    mock_contact_service: ContactService,
    dummy_contact_data: ContactResponse,
) -> None:
    """Test Get Contact Router."""
    # Arrange
    mock_contact_service.get_contact.return_value = dummy_contact_data

    # Act
    with app.extra["container"].contact_service.override(mock_contact_service):
        response = api_client.get("/contacts/dummy_phone_number")

    # Assert
    assert response.status_code == 200


@pytest.mark.parametrize(
    "error, expected_status_code",
    [
        pytest.param(
            InvalidContactParams,
            status.HTTP_400_BAD_REQUEST,
            marks=pytest.mark.parametrize,
            id="Bad Request [400]",
        ),
        pytest.param(
            ContactNotFoundError,
            status.HTTP_404_NOT_FOUND,
            marks=pytest.mark.parametrize,
            id="Not Found [404]",
        ),
        pytest.param(
            Exception,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            marks=pytest.mark.parametrize,
            id="Internal Error [500]",
        ),
    ],
)
def test_get_contact_router_error(
    api_client: TestClient,
    mock_contact_service: ContactService,
    error: Exception,
    expected_status_code: int,
) -> None:
    # Arrange
    mock_contact_service.get_contact.side_effect = error

    # Act
    with app.extra["container"].contact_service.override(mock_contact_service):
        response = api_client.get("/contacts/dummy_phone_number")

    # Assert
    assert response.status_code == expected_status_code


def test_get_contacts_list_router(
    api_client: TestClient,
    mock_contact_service: Mock,
    dummy_contacts_list: List[ContactResponse],
) -> None:
    """Test Get Contacts List Router."""
    # Arrange
    mock_contact_service.get_contacts_list.return_value = dummy_contacts_list

    # Act
    with app.extra["container"].contact_service.override(mock_contact_service):
        response = api_client.get("/contacts")

    # Assert
    assert response.status_code == 200


def test_get_contacts_metadata_route_error(
    api_client: TestClient,
    mock_contact_service: Mock,
) -> None:
    """Test Get router errors."""
    # Arrange
    mock_contact_service.get_contacts_list.side_effect = Exception

    # Act
    with app.extra["container"].contact_service.override(mock_contact_service):
        response = api_client.get("/contacts")

    # Assert
    assert response.status_code == 500


def test_update_contact_router(
    api_client: TestClient,
    mock_contact_service: Mock,
    dummy_updated_contact_data: ContactResponse,
    contact_route_update_request: Dict[str, str],
) -> None:
    """Test Update Contact Router."""
    # Arrange
    mock_contact_service.update_contact.return_value = dummy_updated_contact_data

    # Act
    with app.extra["container"].contact_service.override(mock_contact_service):
        response = api_client.put("/contacts/dummy_phone_number", json=contact_route_update_request)

    # Assert
    assert response.status_code == 200


@pytest.mark.parametrize(
    "error, expected_status_code",
    [
        pytest.param(
            InvalidContactParams,
            status.HTTP_400_BAD_REQUEST,
            marks=pytest.mark.parametrize,
            id="Bad Request [400]",
        ),
        pytest.param(
            ContactNotFoundError,
            status.HTTP_404_NOT_FOUND,
            marks=pytest.mark.parametrize,
            id="Not Found [404]",
        ),
        pytest.param(
            ContactAlreadyExist,
            status.HTTP_409_CONFLICT,
            marks=pytest.mark.parametrize,
            id="Conflict[409]",
        ),
        pytest.param(
            Exception,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            marks=pytest.mark.parametrize,
            id="Internal Error [500]",
        ),
    ],
)
def test_update_contact_route_error(
    api_client: TestClient,
    mock_contact_service: Mock,
    contact_route_update_request: Dict[str, str],
    error: Exception,
    expected_status_code: int,
) -> None:
    """Test Update Contact Route Error."""
    # Arrange
    mock_contact_service.update_contact.side_effect = error
    # Act
    with app.extra["container"].contact_service.override(mock_contact_service):
        response = api_client.put("/contacts/dummy_phone_number", json=contact_route_update_request)

    # Assert
    assert response.status_code == expected_status_code


def test_delete_contact_router(
    api_client: TestClient,
    mock_contact_service: Mock,
    dummy_delete_contact_response: DeleteContactResponse,
) -> DeleteContactResponse:
    """Test Delete Contact Router."""
    # Arrange
    mock_contact_service.delete_contact.return_value = dummy_delete_contact_response

    # Act
    with app.extra["container"].contact_service.override(mock_contact_service):
        response = api_client.delete("/contacts/dummy_phone_number")

    # Assert
    assert response.status_code == 200


@pytest.mark.parametrize(
    "error, expected_status_code",
    [
        pytest.param(
            InvalidContactParams,
            status.HTTP_400_BAD_REQUEST,
            marks=pytest.mark.parametrize,
            id="Bad Request [400]",
        ),
        pytest.param(
            ContactNotFoundError,
            status.HTTP_404_NOT_FOUND,
            marks=pytest.mark.parametrize,
            id="Not Found [404]",
        ),
        pytest.param(
            Exception,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            marks=pytest.mark.parametrize,
            id="Internal Error [500]",
        ),
    ],
)
def test_delete_contact_router_error(
    api_client: TestClient,
    mock_contact_service: Mock,
    error: Exception,
    expected_status_code: int,
) -> None:
    # Arrange
    mock_contact_service.delete_contact.side_effect = error

    # Act
    with app.extra["container"].contact_service.override(mock_contact_service):
        response = api_client.delete("/contacts/dummy_phone_number")

    # Assert
    assert response.status_code == expected_status_code
