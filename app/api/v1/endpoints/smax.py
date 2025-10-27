from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException
from app.logger import logger

#MODELS
from app.models.smax_models import TicketModel
from app.models.auth import AuthModel

router = APIRouter()
security = HTTPBasic()


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> AuthModel:
    """
    Validate HTTP Basic credentials using AuthModel.
    Raises 401 if credentials are invalid.
    """
    auth = AuthModel(username=credentials.username, password=credentials.password)
    if not auth.validate_credentials():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return auth

@router.post("/ticket/create", status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketModel, current_user: AuthModel = Depends(get_current_user)):
    """
    Create a new ticket from SMAX.
    """
    try:
        logger.info(f"Creating ticket with data: {ticket}")
        ticket.add()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Ticket created successfully"})
    except Exception as e:
        logger.error(f"Error creating ticket: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to create ticket"})


@router.post("/ticket/update/{ticket_id}", status_code=status.HTTP_200_OK)
async def update_ticket(ticket_id: str, ticket: TicketModel, current_user: AuthModel = Depends(get_current_user)):
    """
    Update an existing ticket from SMAX.
    """
    try:
        logger.info(f"Updating ticket with ID {ticket_id} and data: {ticket}")
        # ticket.update(ticket_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ticket updated successfully"})
    except Exception as e:
        logger.error(f"Error updating ticket: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to update ticket"})

@router.post("/ticket/close/{ticket_id}", status_code=status.HTTP_200_OK)
async def close_ticket(ticket_id: str, ticket: TicketModel, current_user: AuthModel = Depends(get_current_user)):
    """
    Close an existing ticket from SMAX.
    """
    try:
        logger.info(f"Closing ticket with ID {ticket_id}")
        # ticket.close(ticket_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ticket closed successfully"})
    except Exception as e:
        logger.error(f"Error closing ticket: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to close ticket"})