from fastapi import APIRouter, HTTPException
from app.services.service_factory import ServiceFactory
from app.resources.ticket_resource import TicketResource

router = APIRouter()

@router.get("/health", tags=["health"])
async def health_check():
    # Get the database service for the ticket resource
    data_service = ServiceFactory.get_service("TicketResourceDataService")
    ticket_resource = TicketResource(config=None)

    # Test database connection with a simple query
    try:
        result = data_service.check_connection(ticket_resource.database, ticket_resource.collection)
        return {"status": "connected", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
