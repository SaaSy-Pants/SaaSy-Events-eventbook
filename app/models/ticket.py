from __future__ import annotations
from pydantic import BaseModel, Field


class Ticket(BaseModel):
    TID: str = Field(..., description="Ticket ID")
    EID: str = Field(..., description="Event ID")
    UID: str = Field(..., description="User ID")
    NumGuests: int = Field(1, description="Number of guests")

    class Config:
        json_schema_extra = {
            "example": {
                "TID": "T001",
                "EID": "E001",
                "UID": "U001",
                "NumGuests": 2
            }
        }
