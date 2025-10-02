from sqlalchemy.orm import Session
from models.service import Service
from schemas.service import ServiceCreate, ServiceUpdate


class CRUDService:
    @staticmethod
    def create_service(db: Session, service: ServiceCreate):
        db_service = Service(
            title=service.title,
            description=service.description,
            price=service.price,
            duration_minutes=service.duration_minutes,
            is_active=service.is_active,
        )
        db.add(db_service)
        db.flush()
        db.refresh(db_service)
        return db_service

    @staticmethod
    def get_service(db: Session, service_id: int):
        return db.query(Service).filter(Service.id == service_id).first()

    @staticmethod
    def get_services(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        q: str | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        active: bool | None = None,
    ):
        query = db.query(Service)
        if q:
            query = query.filter(
                Service.title.contains(q) | Service.description.contains(q)
            )
        if price_min is not None:
            query = query.filter(Service.price >= price_min)
        if price_max is not None:
            query = query.filter(Service.price <= price_max)
        if active is not None:
            query = query.filter(Service.is_active == active)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_service(
        db: Session, db_service: Service, service_in: ServiceUpdate
    ):
        update_data = service_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_service, key, value)
        db.flush()
        db.refresh(db_service)
        return db_service

    @staticmethod
    def delete_service(db: Session, db_service: Service):
        db.delete(db_service)
        db.commit()
        return db_service
    
    
service_service = CRUDService()