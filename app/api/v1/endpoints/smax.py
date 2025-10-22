from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.logger import logger

#MODELS
from app.models.smax_models import TicketModel

router = APIRouter()

@router.post("/ticket/create", status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketModel):
    """
    update a new ticket in OpsRamp.
    """
    try:
        logger.info(f"Creating ticket with data: {ticket}")
        ticket.add()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Ticket created successfully"})
    except Exception as e:
        logger.error(f"Error creating ticket: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to create ticket"})


@router.get("/ticket/update/{ticket_id}", status_code=status.HTTP_200_OK)
async def update_ticket(ticket_id: str, ticket: TicketModel):
    """
    Update an existing ticket in OpsRamp.
    """
    try:
        logger.info(f"Updating ticket with ID {ticket_id} and data: {ticket}")
        # ticket.update(ticket_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ticket updated successfully"})
    except Exception as e:
        logger.error(f"Error updating ticket: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to update ticket"})
    
@router.get("/ticket/close/{ticket_id}", status_code=status.HTTP_200_OK)
async def close_ticket(ticket_id: str, ticket: TicketModel):
    """
    Close an existing ticket in OpsRamp.
    """
    try:
        logger.info(f"Closing ticket with ID {ticket_id}")
        # ticket.close(ticket_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Ticket closed successfully"})
    except Exception as e:
        logger.error(f"Error closing ticket: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to close ticket"})