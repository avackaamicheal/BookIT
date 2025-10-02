from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.crud_service import service_service
from database import get_db
from schemas.service import Service, ServiceCreate, ServiceUpdate

router = APIRouter()


@router.get("/", response_model=list[Service])
def get_services(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    q: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    active: bool | None = None,
):
    try: 
        read_service= service_service.get_services(
        db=db, skip=skip, limit=limit, q=q, price_min=price_min, price_max=price_max, active=active
        )
        return read_service

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{service_id}", response_model=Service)
def get_service(service_id: int, db: Session = Depends(get_db)):
    db_service = service_service.get_service(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service


@router.post("/", response_model=Service)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    try:
        created_service= service_service.create_service(db=db, service=service)
        db.commit()
        return created_service
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{service_id}", response_model=Service)
def update_service(
    service_id: int, service: ServiceUpdate, db: Session = Depends(get_db)
):
    db_service = service_service.get_service(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    try: 
        updated_service= service_service.update_service(
        db=db, db_service=db_service, service_in=service
        )
        db.commit()
        return updated_service
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{service_id}", response_model=Service)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = service_service.get_service(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service_service.delete_service(db=db, db_service=db_service)
