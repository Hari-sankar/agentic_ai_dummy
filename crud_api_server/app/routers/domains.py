from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/domains",
    tags=["Domains"]
)

@router.post("/", response_model=schemas.DomainResponse, status_code=status.HTTP_201_CREATED)
def create_domain(domain: schemas.DomainCreate, db: Session = Depends(get_db)):
    db_domain = models.Domain(domain=domain.domain)
    db.add(db_domain)
    db.commit()
    db.refresh(db_domain)
    return db_domain

@router.get("/", response_model=List[schemas.DomainResponse])
def read_domains(
    subdomain_name: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Domain)
    if subdomain_name:
        query = query.join(models.Subdomain).filter(models.Subdomain.subdomain.ilike(f"%{subdomain_name}%"))
    domains = query.offset(skip).limit(limit).all()
    return domains

@router.get("/{domain_id}", response_model=schemas.DomainResponse)
def read_domain(domain_id: uuid.UUID, db: Session = Depends(get_db)):
    db_domain = db.query(models.Domain).filter(models.Domain.id == domain_id).first()
    if db_domain is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found")
    return db_domain

@router.put("/{domain_id}", response_model=schemas.DomainResponse)
def update_domain(domain_id: uuid.UUID, domain: schemas.DomainUpdate, db: Session = Depends(get_db)):
    db_domain = db.query(models.Domain).filter(models.Domain.id == domain_id).first()
    if db_domain is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found")
    
    update_data = domain.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_domain, key, value)
    
    db.add(db_domain)
    db.commit()
    db.refresh(db_domain)
    return db_domain

@router.delete("/{domain_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_domain(domain_id: uuid.UUID, db: Session = Depends(get_db)):
    db_domain = db.query(models.Domain).filter(models.Domain.id == domain_id).first()
    if db_domain is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Domain not found")
    db.delete(db_domain)
    db.commit()
    return {"ok": True}