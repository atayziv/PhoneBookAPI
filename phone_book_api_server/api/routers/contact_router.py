import logging
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from phone_book_api_server.containers import Container
from phone_book_api_server.data_models.contacts import (
    ContactRequest,
    ContactResponse,
    UpdateContactRequest,
)
from phone_book_api_server.data_models.db import DeleteContactResponse
from phone_book_api_server.exceptions.contact import ContactNotFoundError
from phone_book_api_server.services.db_service import DbService

router = APIRouter(
    prefix="",
    tags=["Videos Processor"],
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server Internal Error"},
    },
)


@router.get(
    "/contacts/{contact_phone_number}",
    response_model=ContactResponse,
    description="Get a contact by ID",
)
@inject
def get_existing_contact(
    contact_phone_number: str,
    db_service: DbService = Depends(Provide[Container.db_service]),
) -> ContactResponse:
    """Get a contact by its phone number."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to get contact with his phone number =({contact_phone_number})")
        contact_response = db_service.get_contact(contact_phone_number)
        logger.info(
            f"successfully got contact {contact_response.first_name} {contact_response.last_name})"
        )
        return contact_response
    except ContactNotFoundError as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="contact not found in db"
        ) from error
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        ) from error


@router.get(
    "/contacts/",
    response_model=List[ContactResponse],
    description="Get contacts with pagination",
)
@inject
def get_contacts_with_limit(
    db_service: DbService = Depends(Provide[Container.db_service]),
) -> List[ContactResponse]:
    """Get a contact by its phone number."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to get from db contants with pagination")
        contacts_list_response = db_service.get_contacts_list()
        logger.info(f"successfully got list of contants")
        return contacts_list_response
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        ) from error


@router.post("/contacts", response_model=ContactResponse, description="Create a new contact")
@inject
def create_new_contact(
    contact_data: ContactRequest,
    db_service: DbService = Depends(Provide[Container.db_service]),
) -> None:
    """Create a new contact."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(
            f"Trying to add contact {contact_data.first_name} {contact_data.last_name} to the db"
        )
        contact_response = db_service.create_contact(contact=contact_data)
        logger.info(
            f"Successfully added contact: {contact_data.first_name} {contact_data.last_name}"
        )
        return contact_response
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from error


@router.put(
    "/contacts/{contact_phone_number}",
    response_model=ContactResponse,
    description="Update an existing contact",
)
@inject
def update_existing_contact(
    contact_phone_number: str,
    contact_data: UpdateContactRequest,
    db_service: DbService = Depends(Provide[Container.db_service]),
) -> ContactResponse:
    """Update an existing contact."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to update contact: {contact_data.first_name} {contact_data.last_name}")
        contact_response = db_service.update_contact(
            contact_data=contact_data, contact_phone_number=contact_phone_number
        )
        logger.info(
            f"Successfully updated contact: {contact_data.first_name} {contact_data.last_name}"
        )
        return contact_response
    except ContactNotFoundError as error:
        logger.exception(error)
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="contact not found") from error
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        ) from error


@router.delete(
    "/contacts/{contact_phone_number}",
    response_model=DeleteContactResponse,
    description="Delete a contact by ID",
)
@inject
def delete_existing_contact(
    contact_phone_number: str,
    db_service: DbService = Depends(Provide[Container.db_service]),
) -> DeleteContactResponse:
    """Delete a contact by its ID."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to delete contact with his phone number : {contact_phone_number}")
        delete_response = db_service.delete_contact(contact_phone_number=contact_phone_number)
        logger.info(f"successfully deleted contact whith phone number :  {contact_phone_number})")
        return delete_response
    except ContactNotFoundError as error:
        logger.exception(error)
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="contact not found") from error
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        ) from error
