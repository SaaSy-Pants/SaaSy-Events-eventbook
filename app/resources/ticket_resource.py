from typing import Optional
from app.models.ticket import Ticket
from app.utils.utils import generate_uuid
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
        return result

    def create_ticket(self, tid: str, uid: str, eid: str, num_guests: int):
        ticket = Ticket(TID=tid, UID=uid, EID=eid, NumGuests=num_guests)
        return self.data_service.insert_data_object(self.database, self.collection, ticket)

    def get_tickets_by_user(self, uid: str):
        result = self.data_service.get_data_objects(
            self.database, self.collection, key_field='UID', key_value=uid
        )
        return result

    def cancel_ticket(self, tid: str):
        result = self.data_service.delete_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=tid
        )
        return result