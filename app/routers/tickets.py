from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Form

from app.resources.ticket_resource import TicketResource

router = APIRouter()


@router.post("/book_ticket", tags=["tickets"])
async def book_ticket(uid: Annotated[str, Form()], eid: Annotated[str, Form()]):
    res = TicketResource(config=None)
    result = res.create_ticket(uid, eid)
    return result


@router.get("/{tid}", tags=["tickets"])
async def get_ticket(tid: str):
    res = TicketResource(config=None)
    result = res.get_by_key(tid)
    return result
