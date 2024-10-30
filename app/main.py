from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers import tickets, health
from app.middleware.logging import LoggingMiddleware

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

app.include_router(tickets.router, prefix='/tickets')
app.include_router(health.router)


@app.get("/")
async def root():
    return {"message": "Hello Ticket Booking Application!"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
