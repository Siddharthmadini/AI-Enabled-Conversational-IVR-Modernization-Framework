from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter(prefix="/irctc", tags=["IRCTC Mock APIs"])

class BookTicketReq(BaseModel):
    source: str
    destination: str
    date: str

class PNRReq(BaseModel):
    pnr: str

class TrainStatusReq(BaseModel):
    train_number: str

class TrainAvailabilityReq(BaseModel):
    source: str
    destination: str
    date: str

@router.post("/book-ticket")
async def book_ticket(req: BookTicketReq):
    return {
        "status": "success",
        "pnr": str(random.randint(1000000000, 9999999999)),
        "message": f"Ticket successfully booked from {req.source} to {req.destination} for {req.date}."
    }

@router.post("/reservation-status")
async def reservation_status(req: PNRReq):
    statuses = ["CNF", "RAC", "WL", "CAN"]
    return {
        "pnr": req.pnr,
        "status": random.choice(statuses),
        "passenger_count": random.randint(1, 4),
        "train_number": "12345"
    }

@router.post("/train-running-status")
async def train_running_status(req: TrainStatusReq):
    return {
        "train_number": req.train_number,
        "current_station": "New Delhi",
        "delay_minutes": random.choice([0, 15, 30, 45, 120]),
        "status": "Running"
    }

@router.post("/train-availability")
async def train_availability(req: TrainAvailabilityReq):
    return {
        "source": req.source,
        "destination": req.destination,
        "date": req.date,
        "available_seats": random.randint(0, 250),
        "train_number": "12345",
        "class": "3A"
    }
