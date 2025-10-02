from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.booking import Booking
from schemas.booking import BookingCreate, BookingUpdate
from datetime import datetime

class CRUDBooking:
    @staticmethod
    def create_booking(db: Session, booking: BookingCreate):
        db_booking = Booking(**booking.model_dump())
        db.add(db_booking)
        db.flush()
        db.refresh(db_booking)
        return db_booking

    @staticmethod
    def get_booking(db: Session, booking_id: int):
        return db.query(Booking).filter(Booking.id == booking_id).first()

    @staticmethod
    def get_bookings(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(Booking).filter(Booking.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_all_bookings(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Booking).offset(skip).limit(limit).all()

    @staticmethod
    def update_booking(db: Session, booking_id: int, booking: BookingUpdate):
        db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if db_booking:
            update_data = booking.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_booking, key, value)
            db.flush()
            db.refresh(db_booking)
        return db_booking

    @staticmethod
    def delete_booking(db: Session, booking_id: int):
        db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if db_booking:
            db.delete(db_booking)
            db.commit()
        return db_booking

    @staticmethod
    def get_conflicting_bookings(db: Session, start_time: datetime, end_time: datetime, service_id: int, booking_id: int = None):
        query = db.query(Booking).filter(
            Booking.service_id == service_id,
            Booking.status != 'cancelled',
            and_(
                Booking.start_time < end_time,
                Booking.end_time > start_time
            )
        )
        if booking_id:
            query = query.filter(Booking.id != booking_id)
        return query.all()

booking_service = CRUDBooking()