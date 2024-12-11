from fastapi import APIRouter
from fastapi import Query
from starlette.responses import JSONResponse
import random

from app.resources.ticket_resource import TicketResource
from app.utils.utils import generate_uuid

router = APIRouter()


@router.post("", tags=["tickets"])
async def book_ticket(booking_details: dict):
    res = TicketResource(config=None)
    try:
        tid = str(generate_uuid())
        result = res.create_ticket(tid, booking_details['uid'], booking_details['eid'], booking_details['num_guests'])
        if result['error'] is not None:
            if result['status'] == 'bad request':
                return JSONResponse(content=result, status_code=400)
            else:
                return JSONResponse(content=result, status_code=500)
        else:
            result['TID'] = tid
            return JSONResponse(content=result, status_code=201)
    except AttributeError:
        return JSONResponse(content='Bad Request', status_code=400)

@router.get("/{tid}", tags=["tickets"])
async def get_ticket(tid: str):
    res = TicketResource(config=None)
    result = res.get_by_key(tid)
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=404)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result['details'], status_code=200)

@router.get("", tags=["tickets"])
async def get_tickets_by_user(
    uid: str, 
    limit: int = Query(10, le=100),  # Default limit is 10, maximum 100
    offset: int = Query(0, ge=0)     # Default offset is 0, no negative offsets
):
    res = TicketResource(config=None)
    result = res.get_tickets_by_user(uid, limit, offset)

    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        else:
            return JSONResponse(content={"error": "Database error"}, status_code=500)
    else:
        return JSONResponse(content={"tickets": result['result']}, status_code=200)

@router.get("/event/{eid}/users", tags=["users"])
async def get_users_by_event(
    eid: str, 
    limit: int = Query(10, le=100),  # Default limit is 10, maximum 100
    offset: int = Query(0, ge=0)     # Default offset is 0, no negative offsets
):
    res = TicketResource(config=None)
    result = res.get_users_by_event(eid, limit, offset)

    print(result)

    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content={"error": "Event not found"}, status_code=404)
        else:
            return JSONResponse(content={"error": "Database error"}, status_code=500)
    else:
        return JSONResponse(content={"uids": result['result']}, status_code=200)


@router.delete("/{tid}", tags=["tickets"])
async def cancel_ticket(tid: str):
    res = TicketResource(config=None)
    result = res.cancel_ticket(tid)
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content={"error": "Ticket not found"}, status_code=404)
        else:
            return JSONResponse(content={"error": "Database error"}, status_code=500)
    else:
        return JSONResponse(content={"message": "Deletion successful"}, status_code=200)

