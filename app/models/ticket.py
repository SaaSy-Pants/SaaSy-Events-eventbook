from __future__ import annotations
from pydantic import BaseModel, Field


class Ticket(BaseModel):
    TID: str = Field(..., max_length=5, description="Ticket ID")
    EID: str = Field(..., max_length=5, description="Event ID")
    UID: str = Field(..., max_length=5, description="User ID")
    QRLink: str = Field(..., max_length=255, description="QR Code Link")

    class Config:
        json_schema_extra = {
            "example": {
                "TID": "T001",
                "EID": "E001",
                "UID": "U001",
                "QRLink": "https://example.com/qr/T001"
            }
        }
