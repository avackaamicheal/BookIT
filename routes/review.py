
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.review import Review, ReviewCreate, ReviewUpdate
from crud.crud_review import review_service
from database import get_db
from security import get_current_user
from models.user import User
from models.booking import Booking
from models.review import Review as ReviewModel

router = APIRouter()

@router.post("/reviews", response_model=Review)
def create_review(review: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        booking = db.query(Booking).filter(Booking.id == review.booking_id, Booking.user_id == current_user.id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found or you are not the owner")
        if booking.status != "completed":
            raise HTTPException(status_code=400, detail="Booking is not completed")
        existing_review = db.query(ReviewModel).filter(ReviewModel.booking_id == review.booking_id).first()
        if existing_review:
            raise HTTPException(status_code=400, detail="A review for this booking already exists")
        created_review= review_service.create_review(db=db, review=review, user_id=current_user.id)
        db.commit()
        return created_review
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/services/{service_id}/reviews", response_model=list[Review])
def read_reviews_for_service(service_id: int, db: Session = Depends(get_db)):
    try:
        reviews = review_service.get_reviews_by_service(db, service_id=service_id)
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/reviews/{review_id}", response_model=Review)
def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        db_review = review_service.get_review(db, review_id)
        if not db_review:
            raise HTTPException(status_code=404, detail="Review not found")
        if db_review.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this review")
        updated_review= review_service.update_review(db=db, review_id=review_id, review=review)
        db.commit()
        return updated_review
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/reviews/{review_id}", response_model=Review)
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        db_review = review_service.get_review(db, review_id)
        if not db_review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        booking = db.query(Booking).filter(Booking.id == db_review.booking_id).first()

        if booking.user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Not authorized to delete this review")
            
        review_service.delete_review(db=db, review_id=review_id)
        return db_review
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
