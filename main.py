from fastapi import FastAPI
from routes import user, service, booking, review, auth
import models.user, models.booking, models.service, models.review
from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    
    title= "BookIt API System",
    description="API for managing serives, bookings, users, and reviews",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
    )

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(service.router, prefix="/services", tags=["services"])
app.include_router(booking.router, prefix="/bookings", tags=["bookings"])
app.include_router(review.router, prefix="/reviews", tags=["reviews"])


@app.get("/")
def read_root():
    return {"BOOKIT": "Booking Api"}
