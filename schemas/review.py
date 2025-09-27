from pydantic import BaseModel
from datetime import datetime

class ReviewBase(BaseModel):
    booking_id: int
    rating: int
    comment: str

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None

class Review(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
