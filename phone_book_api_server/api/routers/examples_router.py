import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path

from phone_book_api_server.containers import Container
from phone_book_api_server.data_models.contacts import ContactResponse
from phone_book_api_server.services.api_service import ApiService

router = APIRouter(
    prefix="",
    tags=["contacts"],
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)


# @router.get("/{contact_id}", response_model=contact, description="Get a contact by ID")
# async def get_contact(
#     contact_id: str = Path(..., title="The ID of the contact to get"),
#     contact_service: contactService = Depends(Container.contact_service),
# ) -> contact:
#     """Get a contact by its ID."""
#     logger = logging.getLogger(__name__)
#     try:
#         return contact_service.get_contact(contact_id)
#     except contactNotFoundError as error:
#         logger.exception(error)
#         raise HTTPException(status_code=404, detail="contact not found") from error
#     except Exception as error:
#         logger.exception(error)
#         raise HTTPException(status_code=500, detail="Internal Server Error") from error


@router.post("/contacts", response_model=ContactResponse, description="Create a new contact")
def create_contact(
    contact_data: contactCreate,
) -> ContactResponse:
    """Create a new contact."""
    logger = logging.getLogger(__name__)
    try:
        return contact_service.create_contact(contact_data)
    except Exception as error:
        logger.exception(error)
        raise HTTPException(status_code=500, detail="Internal Server Error") from error


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
