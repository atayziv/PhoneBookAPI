import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from phone_book_api_server.containers import Container
from phone_book_api_server.data_models.contacts import ContactRequest, ContactResponse
from phone_book_api_server.exceptions.contact import ContactNotFoundError
from phone_book_api_server.services.api_service import ApiService

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
    "/contacts/{contact_id}", response_model=ContactResponse, description="Get a contact by ID"
)
@inject
def get_contact(
    contact_phone_number: str,
    api_service: ApiService = Depends(Provide[Container.api_service]),
) -> ContactResponse:
    """Get a contact by its phone number."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to get contact with his phone number =({contact_phone_number})")
        contact = api_service.get_contact_data(contact_phone_number)
        logger.info(f"successfully get contact with number =({contact_phone_number})")
        return contact
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


@router.post("/contacts", description="Create a new contact")
@inject
def create_contact(
    contact_data: ContactRequest,
    api_service: ApiService = Depends(Provide[Container.api_service]),
) -> None:
    """Create a new contact."""
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Trying to add new contact")
        api_service.insert_contact_data(contact_data)
        logger.info(f"Successfully added contact: {contact_data.first_name}")
    except Exception as error:
        logger.exception(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ProcessVideos Internal Server Error",
        ) from error


# @router.put("/{contact_id}", response_model=contact, description="Update an existing contact")
# async def update_contact(
#     contact_id: str = Path(..., title="The ID of the contact to update"),
#     contact_data: contactUpdate,
#     contact_service: contactService = Depends(Container.contact_service),
# ) -> contact:
#     """Update an existing contact."""
#     logger = logging.getLogger(__name__)
#     try:
#         return contact_service.update_contact(contact_id, contact_data)
#     except contactNotFoundError as error:
#         logger.exception(error)
#         raise HTTPException(status_code=404, detail="contact not found") from error
#     except Exception as error:
#         logger.exception(error)
#         raise HTTPException(status_code=500, detail="Internal Server Error") from error


# @router.delete("/{contact_id}", description="Delete a contact by ID")
# async def delete_contact(
#     contact_id: str = Path(..., title="The ID of the contact to delete"),
#     contact_service: contactService = Depends(Container.contact_service),
# ) -> None:
#     """Delete a contact by its ID."""
#     logger = logging.getLogger(__name__)
#     try:
#         contact_service.delete_contact(contact_id)
#     except contactNotFoundError as error:
#         logger.exception(error)
#         raise HTTPException(status_code=404, detail="contact not found") from error
#     except Exception as error:
#         logger.exception(error)
#         raise HTTPException(status_code=500, detail="Internal Server Error") from error
