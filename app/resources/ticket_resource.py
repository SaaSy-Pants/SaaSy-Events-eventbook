from typing import Optional
from app.models.ticket import Ticket
from framework.resources.base_resource import BaseResource
from app.services.service_factory import ServiceFactory

class TicketResource(BaseResource):
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config)
        # Dependency injection for data service
        self.data_service = ServiceFactory.get_service("TicketResourceDataService")
        self.database = "TICKETS"  # Database name
        self.collection = "tick_tab"  # Collection name
        self.key_field = "TID"  # Key field for ticket identification

    def get_by_key(self, tid: str) -> Optional[Ticket]:
        # Query ticket details by TID from the database
        result = self.data_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=tid
        )
        if result:
            return Ticket(**result)
        return None

    def create_ticket(self, uid: str, eid: str):
        # TODO: generate TID as an UUID and a functional QRLink
        ticket = Ticket(TID="T007", UID=uid, EID=eid, QRLink="test_link")
        return self.data_service.insert_data_object(self.database, self.collection, ticket)
