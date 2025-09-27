from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class BookingBase(BaseModel):
    user_id: int
    service_id: int
    start_time: datetime
    end_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: BookingStatus | None = None

class Booking(BookingBase):
    id: int
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True
