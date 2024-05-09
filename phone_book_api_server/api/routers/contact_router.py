import logging

from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from phone_book_api_server.clients.db_client import (
    create_contact,
    delete_contact,
    get_contact,
    update_contact,
)
from phone_book_api_server.data_models.contacts import (
    ContactRequest,
    ContactResponse,
    UpdateContactRequest,
)
from phone_book_api_server.data_models.db import DeleteContactResponse
from phone_book_api_server.database.connection import get_db
from phone_book_api_server.exceptions.contact import ContactNotFoundError

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
    db: Session = Depends(get_db),
) -> ContactResponse:
    """Get a contact by its phone number."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to get contact with his phone number =({contact_phone_number})")
        contact_response = get_contact(db=db, contact_phone_number=contact_phone_number)
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


@router.post("/contacts", response_model=ContactResponse, description="Create a new contact")
@inject
def create_new_contact(
    contact_data: ContactRequest,
    db: Session = Depends(get_db),
) -> None:
    """Create a new contact."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(
            f"Trying to add contact {contact_data.first_name} {contact_data.last_name} to the db"
        )
        contact_response = create_contact(db=db, contact=contact_data)
        logger.info(
            f"Successfully added contact: {contact_data.first_name} {contact_data.last_name}"
        )
        return contact_response
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ProcessVideos Internal Server Error",
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
    db: Session = Depends(get_db),
) -> ContactResponse:
    """Update an existing contact."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to update contact: {contact_data.first_name} {contact_data.last_name}")
        contact_response = update_contact(
            db=db, contact_data=contact_data, contact_phone_number=contact_phone_number
        )
        logger.info(
            f"Successfully updated contact: {contact_data.first_name} {contact_data.last_name}"
        )
        return contact_response
    except ContactNotFoundError as error:
        logger.exception(error)
        raise HTTPException(status_code=404, detail="contact not found") from error
    except Exception as error:
        logger.exception(error)
        raise HTTPException(status_code=500, detail="Internal Server Error") from error


@router.delete(
    "/contacts/{contact_phone_number}",
    response_model=DeleteContactResponse,
    description="Delete a contact by ID",
)
@inject
def delete_existing_contact(
    contact_phone_number: str,
    db: Session = Depends(get_db),
) -> DeleteContactResponse:
    """Delete a contact by its ID."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to delete contact with his phone number : {contact_phone_number}")
        delete_response = delete_contact(db=db, contact_phone_number=contact_phone_number)
        logger.info(f"successfully deleted contact whith phone number :  {contact_phone_number})")
        return delete_response
    except ContactNotFoundError as error:
        logger.exception(error)
        raise HTTPException(status_code=404, detail="contact not found") from error
    except Exception as error:
        logger.exception(error)
        raise HTTPException(status_code=500, detail="Internal Server Error") from error
