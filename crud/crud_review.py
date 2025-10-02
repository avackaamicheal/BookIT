from sqlalchemy.orm import Session
from models.review import Review
from models.booking import Booking
from schemas.review import ReviewCreate, ReviewUpdate

class CRUDReview:
    @staticmethod
    def create_review(db: Session, review: ReviewCreate, user_id: int):
        db_review = Review(**review.dict(), user_id=user_id)
        db.add(db_review)
        db.flush()
        db.refresh(db_review)
        return db_review

    @staticmethod
    def get_review(db: Session, review_id: int):
        return db.query(Review).filter(Review.id == review_id).first()

    @staticmethod
    def get_reviews_by_service(db: Session, service_id: int):
        return db.query(Review).join(Booking).filter(Booking.service_id == service_id).all()

    @staticmethod
    def update_review(db: Session, review_id: int, review: ReviewUpdate):
        db_review = CRUDReview.get_review(db, review_id)
        if db_review:
            for key, value in review.dict().items():
                setattr(db_review, key, value)
            db.flush()
            db.refresh(db_review)
        return db_review

    @staticmethod
    def delete_review(db: Session, review_id: int):
        db_review = CRUDReview.get_review(db, review_id)
        if db_review:
            db.delete(db_review)
            db.commit()
        return db_review

review_service = CRUDReview()