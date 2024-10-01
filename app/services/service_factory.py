from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
from framework.services.service_factory import BaseServiceFactory


class ServiceFactory(BaseServiceFactory):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_service(cls, service_name):
        if service_name == 'TicketResourceDataService':
            # Database connection context for MySQLRDBDataService
            context = {
                'user': "root",
                'password': "dbuserdbuser",
                'host': "localhost",
                'port': 3306,
            }
            data_service = MySQLRDBDataService(context=context)
            result = data_service
        else:
            result = None

        return result
