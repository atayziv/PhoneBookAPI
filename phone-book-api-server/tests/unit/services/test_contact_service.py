from typing import List
from unittest import mock
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from phone_book_api_server.data_models.contacts import ContactResponse
from phone_book_api_server.data_models.db import DeleteContactResponse
from phone_book_api_server.exceptions.contact import (
    InvalidContactEmail,
    InvalidContactName,
    InvalidContactNumber,
)
from phone_book_api_server.services.contact_service import ContactService


def test_insert_contact(
    mocker: MockerFixture,
    contact_service: ContactService,
    dummy_contact_data: ContactResponse,
    mock_db_client: Mock,
) -> None:
    """Test Insert Contact With Valid Params"""
    # Arrange
    mock_db_client.insert_contact.return_value = None
    mocker.patch(
        "phone_book_api_server.services.contact_service.ContactService.get_contact",
        return_value=dummy_contact_data,
    )
    # Act
    with mock.patch("builtins.open", mock.mock_open()) as _:
        contact_service.insert_contact(dummy_contact_data)


def test_insert_contact_without_email_address(
    mocker: MockerFixture,
    contact_service: ContactService,
    dummy_contact_data_without_email: ContactResponse,
    mock_db_client: Mock,
) -> None:
    """Test Insert Contact With Valid Params"""
    # Arrange
    mock_db_client.insert_contact.return_value = None
    mocker.patch(
        "phone_book_api_server.services.contact_service.ContactService.get_contact",
        return_value=dummy_contact_data_without_email,
    )
    # Act
    with mock.patch("builtins.open", mock.mock_open()) as _:
        contact_service.insert_contact(dummy_contact_data_without_email)


def test_insert_contact_with_invalid_phone_error(
    contact_service: ContactService,
    dummy_contact_invalid_number: ContactResponse,
) -> None:
    """Test Insert Contact With Valid Params"""
    # Act And Assert
    with pytest.raises(InvalidContactNumber):
        with mock.patch("builtins.open", mock.mock_open()) as _:
            contact_service.insert_contact(dummy_contact_invalid_number)


def test_insert_contact_with_invalid_email_error(
    contact_service: ContactService,
    dummy_contact_invalid_email: ContactResponse,
) -> None:
    """Test Insert Contact With Valid Params"""
    # Act And Assert
    with pytest.raises(InvalidContactEmail):
        with mock.patch("builtins.open", mock.mock_open()) as _:
            contact_service.insert_contact(dummy_contact_invalid_email)


def test_insert_contact_with_invalid_name_error(
    contact_service: ContactService,
    dummy_contact_invalid_name: ContactResponse,
) -> None:
    """Test Insert Contact With Valid Params"""
    # Act And Assert
    with pytest.raises(InvalidContactName):
        with mock.patch("builtins.open", mock.mock_open()) as _:
            contact_service.insert_contact(dummy_contact_invalid_name)


def test_get_contacts_list(
    contact_service: ContactService,
    mock_db_client: Mock,
    dummy_contacts_list: List[ContactResponse],
    limit_list_size_response: int,
) -> None:
    """Test Get Contacts List With Pagination Validation."""
    # Arrange
    mock_db_client.get_contacts.return_value = dummy_contacts_list
    # Act
    with mock.patch("builtins.open", mock.mock_open()) as _:
        contact_service.get_contacts_list(limit_list_size_response)


@pytest.mark.parametrize(
    "dummy_phone_number, is_valid",
    [
        ("+972546643567", True),
        ("0546643567", False),
    ],
    ids=["valid_phone_number", "invalid_phone_number"],
)
def test_get_contact(
    mocker: MockerFixture,
    contact_service: ContactService,
    dummy_contact_data: ContactResponse,
    mock_db_client: Mock,
    dummy_phone_number: str,
    is_valid: bool,
) -> None:
    """Test Get Contact."""
    # Arrange
    mocker.patch(
        "phone_book_api_server.services.contact_service.ContactService._is_valid_number",
        return_value=is_valid,
    )
    # Act & Assert
    if is_valid:
        mock_db_client.get_contact.return_value = dummy_contact_data
        with mock.patch("builtins.open", mock.mock_open()) as _:
            contact_service.get_contact(dummy_phone_number)
    else:
        with pytest.raises(InvalidContactNumber):
            with mock.patch("builtins.open", mock.mock_open()) as _:
                contact_service.get_contact(dummy_phone_number)


def test_update_contact(
    mocker: MockerFixture,
    contact_service: ContactService,
    mock_db_client: Mock,
    dummy_contact_data: ContactResponse,
    dummy_phone_number: str,
) -> None:
    # Arrange
    mocker.patch(
        "phone_book_api_server.services.contact_service.ContactService.get_contact",
        return_value=dummy_contact_data,
    )
    mock_db_client.get_contact.return_value = dummy_contact_data
    # Act
    with mock.patch("builtins.open", mock.mock_open()) as _:
        contact_service.update_contact(dummy_contact_data, dummy_phone_number)


@pytest.mark.parametrize(
    "error_validation",
    [
        "phone_error",
        "email_error",
        "name_error",
    ],
    ids=["invalid_number", "invalid_email", "invalid_name"],
)
def test_update_contact_with_errors(
    mocker: MockerFixture,
    contact_service: ContactService,
    dummy_contact_data: ContactResponse,
    dummy_phone_number: str,
    error_validation: str,
) -> None:
    # Arrange
    mocker.patch(
        "phone_book_api_server.services.contact_service.ContactService.get_contact",
        return_value=dummy_contact_data,
    )
    # Act & Assert
    if error_validation == "phone_error":
        mocker.patch(
            "phone_book_api_server.services.contact_service.ContactService._is_valid_number",
            side_effect=InvalidContactNumber("Invalid phone number."),
        )
        with pytest.raises(InvalidContactNumber):
            with mock.patch("builtins.open", mock.mock_open()) as _:
                contact_service.update_contact(dummy_contact_data, dummy_phone_number)
    elif error_validation == "email_error":
        mocker.patch(
            "phone_book_api_server.services.contact_service.ContactService._is_valid_email",
            side_effect=InvalidContactEmail("Invalid contact email address."),
        )
        with pytest.raises(InvalidContactEmail):
            with mock.patch("builtins.open", mock.mock_open()) as _:
                contact_service.update_contact(dummy_contact_data, dummy_phone_number)
    elif error_validation == "name_error":
        mocker.patch(
            "phone_book_api_server.services.contact_service.ContactService._is_valid_name",
            side_effect=InvalidContactName(detail="Invalid contact name."),
        )
        with pytest.raises(InvalidContactName):
            with mock.patch("builtins.open", mock.mock_open()) as _:
                contact_service.update_contact(dummy_contact_data, dummy_phone_number)


@pytest.mark.parametrize(
    "is_valid",
    [
        True,
        False,
    ],
    ids=["valid_phone_number", "invalid_phone_number"],
)
def test_delete_contact(
    mocker: MockerFixture,
    mock_db_client: Mock,
    dummy_phone_number: str,
    dummy_contact_data: ContactResponse,
    contact_service: ContactService,
    is_valid: bool,
    delete_contact_response_successfuly: DeleteContactResponse,
) -> None:
    # Arrange
    mocker.patch(
        "phone_book_api_server.services.contact_service.ContactService._is_valid_number",
        return_value=is_valid,
    )
    mocker.patch(
        "phone_book_api_server.services.contact_service.ContactService.get_contact",
        return_value=dummy_contact_data,
    )
    mock_db_client.get_contact.return_value = dummy_contact_data

    # Act and Assert
    if is_valid:
        response = contact_service.delete_contact(dummy_phone_number)
        assert response == delete_contact_response_successfuly

    else:
        with pytest.raises(InvalidContactNumber):
            with mock.patch("builtins.open", mock.mock_open()) as _:
                contact_service.delete_contact(dummy_phone_number)
