from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Form
from starlette.responses import JSONResponse

from app.resources.ticket_resource import TicketResource

router = APIRouter()


@router.post("", tags=["tickets"])
async def book_ticket(uid: Annotated[str, Form()], eid: Annotated[str, Form()], num_guests: Annotated[int, Form()]):
    res = TicketResource(config=None)
    result = res.create_ticket(uid, eid, num_guests)
    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content=result, status_code=400)
        else:
            return JSONResponse(content=result, status_code=500)
    else:
        return JSONResponse(content=result, status_code=201)


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
async def get_tickets_by_user(uid: str):
    res = TicketResource(config=None)
    result = res.get_tickets_by_user(uid)

    if result['error'] is not None:
        if result['status'] == 'bad request':
            return JSONResponse(content={"error": "User not found"}, status_code=404)
        else:
            return JSONResponse(content={"error": "Database error"}, status_code=500)
    else:
        return JSONResponse(content={"tickets": result['tickets']}, status_code=200)


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

