from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from schemas import booking as booking_schema
from crud.crud_booking import booking_service
from models import user as user_model
from security import get_current_user

router = APIRouter()

@router.post("/", response_model=booking_schema.Booking)
def create_booking(
    booking: booking_schema.BookingCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """
    Create a new booking.
    """
    try:
        # Validate overlaps/conflicts
        conflicting_bookings = booking_service.get_conflicting_bookings(
            db,
            start_time=booking.start_time,
            end_time=booking.end_time,
            service_id=booking.service_id,
        )
        if conflicting_bookings:
            raise HTTPException(status_code=409, detail="Booking conflict")

        booking.user_id = current_user.id
        created_booking= booking_service.create_booking(db=db, booking=booking)
        db.commit()
        return created_booking
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[booking_schema.Booking])
def get_bookings(
    status: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """
    Retrieve bookings.
    - Users can only see their own bookings.
    - Admins can see all bookings and filter by status, from_date, and to_date.
    """
    try:
        if current_user.role == user_model.Role.admin:
            return booking_service.get_all_bookings(db, status=status, from_date=from_date, to_date=to_date)
        else:
            return booking_service.get_bookings(db, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{booking_id}", response_model=booking_schema.Booking)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """
    Retrieve a specific booking.
    - Users can only retrieve their own bookings.
    - Admins can retrieve any booking.
    """
    try:
        db_booking = booking_service.get_booking(db, booking_id=booking_id)
        if db_booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")
        if not current_user.role == user_model.Role.admin and db_booking.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to access this booking")
        return db_booking
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{booking_id}", response_model=booking_schema.Booking)
def update_booking(
    booking_id: int,
    booking: booking_schema.BookingUpdate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """
    Update a booking.
    - Owner can reschedule/cancel if pending or confirmed.
    - Admin can update status.
    """
    try:
        db_booking = booking_service.get_booking(db, booking_id=booking_id)
        if db_booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")

        is_owner = db_booking.user_id == current_user.id
        is_admin = current_user.role == user_model.Role.admin

        if not is_owner and not is_admin:
            raise HTTPException(status_code=403, detail="Not authorized to update this booking")

        if is_owner:
            if db_booking.status not in ["pending", "confirmed"]:
                raise HTTPException(status_code=403, detail="Booking cannot be rescheduled or cancelled in its current status")
            if booking.status and booking.status not in ["pending", "cancelled"]:
                raise HTTPException(status_code=403, detail="You can only change the status to 'pending' or 'cancelled'")

        if is_admin:
            if booking.status and booking.status not in ["pending", "confirmed", "cancelled"]:
                raise HTTPException(status_code=403, detail="Invalid status")

        # Validate overlaps/conflicts if rescheduling
        if booking.start_time and booking.end_time:
            conflicting_bookings = booking_service.get_conflicting_bookings(
                db,
                start_time=booking.start_time,
                end_time=booking.end_time,
                service_id=db_booking.service_id,
                booking_id=booking_id,
            )
            if conflicting_bookings:
                raise HTTPException(status_code=409, detail="Booking conflict")

        updated_booking= booking_service.update_booking(db=db, booking_id=booking_id, booking=booking)
        db.commit()
        return updated_booking
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{booking_id}", response_model=booking_schema.Booking)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user),
):
    """
    Delete a booking.
    - Owner can delete before start_time.
    - Admin can delete anytime.
    """
    try:
        db_booking = booking_service.get_booking(db, booking_id=booking_id)
        if db_booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")

        is_owner = db_booking.user_id == current_user.id
        is_admin = current_user.role == user_model.Role.admin

        if not is_owner and not is_admin:
            raise HTTPException(status_code=403, detail="Not authorized to delete this booking")

        if is_owner and datetime.utcnow() >= db_booking.start_time:
            raise HTTPException(status_code=403, detail="Cannot delete a booking that has already started")

        return booking_service.delete_booking(db=db, booking_id=booking_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))