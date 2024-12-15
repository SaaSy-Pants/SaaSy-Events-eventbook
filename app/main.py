from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers import tickets, health
from app.middleware.logging import LoggingMiddleware

from app.rabbitmq.rabbitmq_consumer import EventUpdateListener  # Import RMQ listener
import threading

EVENT_MANAGEMENT_URL = "localhost"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Logging Middleware
app.add_middleware(LoggingMiddleware)


app.include_router(tickets.router, prefix='/ticket')
app.include_router(health.router)

# Function to start the RabbitMQ listener in a background thread
def start_event_update_listener():
    listener = EventUpdateListener(rabbitmq_server=EVENT_MANAGEMENT_URL, queue_name="event_updates")
    listener.listen_for_event_updates()

# Start the RabbitMQ listener in a background thread
thread = threading.Thread(target=start_event_update_listener)
thread.daemon = True  # Ensures the thread will exit when the program does
thread.start()

@app.get("/")
async def root():
    return {"message": "Hello Ticket Booking Application!"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)
