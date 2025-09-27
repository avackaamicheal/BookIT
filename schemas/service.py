from pydantic import BaseModel
from datetime import datetime

class ServiceBase(BaseModel):
    title: str
    description: str
    price: float
    duration_minutes: int
    is_active: bool = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    duration_minutes: int | None = None
    is_active: bool | None = None

class Service(ServiceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
