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
from phone_book_api_server.exceptions.contact import (
    ContactAlreadyExist,
    ContactNotFoundError,
    InvalidContactParams,
)
from phone_book_api_server.services.contact_service import ContactService

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts Processor"],
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server Internal Error"},
    },
)


@router.get(
    "/{contact_phone_number}",
    response_model=ContactResponse,
    description="Get a contact by ID",
)
@inject
def get_contact(
    contact_phone_number: str,
    contact_service: ContactService = Depends(Provide[Container.contact_service]),
) -> ContactResponse:
    """Get a contact by its phone number."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to get contact with his phone number =({contact_phone_number})")
        contact_response = contact_service.get_contact(contact_phone_number)
        logger.info(
            f"successfully got contact {contact_response.first_name} {contact_response.last_name})"
        )
        return contact_response
    except InvalidContactParams as error:
        logger.exception(error)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
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
    "/",
    response_model=List[ContactResponse],
    description="Get contacts with pagination",
)
@inject
def get_contacts_with_limit(
    config=Depends(Provide[Container.config]),
    contact_service: ContactService = Depends(Provide[Container.contact_service]),
) -> List[ContactResponse]:
    """Get a contact by its phone number."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to get from db contants with pagination")
        contacts_list_response = contact_service.get_contacts_list(
            config.get("limit_contacts_list")
        )
        logger.info(f"successfully got list of contants")
        return contacts_list_response
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        ) from error


@router.post("/", response_model=ContactResponse, description="Create a new contact")
@inject
def create_contact(
    contact_data: ContactRequest,
    contact_service: ContactService = Depends(Provide[Container.contact_service]),
) -> None:
    """Create a new contact."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(
            f"Trying to add contact {contact_data.first_name} {contact_data.last_name} to the db"
        )
        contact_response = contact_service.insert_contact(contact_data)
        logger.info(
            f"Successfully added contact: {contact_data.first_name} {contact_data.last_name}"
        )
        return contact_response
    except InvalidContactParams as error:
        logger.exception(error)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    except ContactAlreadyExist as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Contact Already Exist in db."
        ) from error
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from error


@router.put(
    "/{contact_phone_number}",
    response_model=ContactResponse,
    description="Update an existing contact",
)
@inject
def update_contact(
    contact_phone_number: str,
    contact_data: UpdateContactRequest,
    contact_service: ContactService = Depends(Provide[Container.contact_service]),
) -> ContactResponse:
    """Update an existing contact."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to update contact: {contact_data.first_name} {contact_data.last_name}")
        contact_response = contact_service.update_contact(contact_data, contact_phone_number)
        logger.info(
            f"Successfully updated contact: {contact_data.first_name} {contact_data.last_name}"
        )
        return contact_response
    except InvalidContactParams as error:
        logger.exception(error)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    except ContactNotFoundError as error:
        logger.exception(error)
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="contact not found") from error
    except ContactAlreadyExist as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Contact Already Exist in db."
        ) from error
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        ) from error


@router.delete(
    "/{contact_phone_number}",
    response_model=DeleteContactResponse,
    description="Delete a contact by ID",
)
@inject
def delete_contact(
    contact_phone_number: str,
    contact_service: ContactService = Depends(Provide[Container.contact_service]),
) -> DeleteContactResponse:
    """Delete a contact by its ID."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to delete contact with his phone number : {contact_phone_number}")
        delete_response = contact_service.delete_contact(contact_phone_number=contact_phone_number)
        logger.info(f"successfully deleted contact whith phone number :  {contact_phone_number})")
        return delete_response
    except InvalidContactParams as error:
        logger.exception(error)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    except ContactNotFoundError as error:
        logger.exception(error)
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="contact not found") from error
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        ) from error
