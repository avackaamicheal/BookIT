from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate


class CRUDUser:
    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        from security import get_password_hash
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email, 
            name=user.name, 
            password_hash=hashed_password)
        db.add(db_user)
        db.flush()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, db_user: User, user_in: UserUpdate):
        if user_in.name:
            db_user.name = user_in.name
        if user_in.email:
            db_user.email = user_in.email
        db.flush()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, db_user: User):
        db.delete(db_user)
        db.commit()
        return db_user


user_service = CRUDUser()
