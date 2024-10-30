from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.routers import tickets, health

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

app.include_router(tickets.router, prefix='/ticket')
app.include_router(health.router)


@app.get("/")
async def root():
    return {"message": "Hello Ticket Booking Application!"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)
