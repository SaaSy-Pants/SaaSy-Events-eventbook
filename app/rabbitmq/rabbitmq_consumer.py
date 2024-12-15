import pika
import json
from app.resources.ticket_resource import TicketResource  # Assuming this is where your methods are

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

USER_MANAGEMENT_URL = "localhost:8003"

class EventUpdateListener:
    def __init__(self, rabbitmq_server: str, queue_name: str):
        # RabbitMQ Consumer setup
        self.rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_server))
        self.channel = self.rabbitmq_connection.channel()

        # Declare the same exchange as the publisher
        self.channel.exchange_declare(exchange='event_updates', exchange_type='fanout')

        # Create a temporary queue for receiving messages
        result = self.channel.queue_declare('', exclusive=True)
        self.queue_name = result.method.queue

        # Bind the queue to the exchange
        self.channel.queue_bind(exchange='event_updates', queue=self.queue_name)

        # Set up the callback for consuming messages
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message, auto_ack=True)
        self.ticket_resource = TicketResource(config=None)  # Initialize TicketResource

        self.stepfunctions_client = boto3.client('stepfunctions', region_name='us-east-1')

    def listen_for_event_updates(self):
        print('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def on_message(self, ch, method, properties, body):
        event_update = json.loads(body)
        event_id = event_update.get('event_id')
        updated_data = event_update.get('updated_data')
        
        if event_id:
            print(f"Received update for event ID {event_id}: {updated_data}")
            self.process_event_update(event_id)
    
    # def trigger_step_function(self, user_ids: list):
    #     try:
    #         # Start the Step Function execution
    #         response = self.stepfunctions_client.start_execution(
    #             stateMachineArn='arn:aws:states:us-east-1:123456789012:stateMachine:EventNotificationWorkflow',
    #             input=json.dumps({'user_ids': user_ids})
    #         )
    #         print(response)
    #         print(f"Step Function triggered. Execution ARN: {response['executionArn']}")
    #     except NoCredentialsError:
    #         print("AWS credentials not found. Please configure credentials.")
    #     except PartialCredentialsError:
    #         print("Incomplete AWS credentials. Please check your setup.")
    #     except Exception as e:
    #         print(f"Error triggering Step Function {str(e)}")

    def process_event_update(self, event_id: str):
        try:
            # Call TicketResource to get users for the event
            users = self.ticket_resource.get_users_by_event(event_id, 100000, 0)

            if users['error'] == None:
                print(f"Users for event {event_id}: {users}")
                user_ids = [user.get('UID') for user in users['result']]
            else:
                print(users['error'])
                return
            
            # self.trigger_step_function(user_ids)
            
        except Exception as e:
            print(f"Error processing event {event_id}: {str(e)}")
