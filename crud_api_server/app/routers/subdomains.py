from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import uuid

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/subdomains",
    tags=["Subdomains"]
)

@router.post("/", response_model=schemas.SubdomainResponse, status_code=status.HTTP_201_CREATED)
def create_subdomain(subdomain: schemas.SubdomainCreate, db: Session = Depends(get_db)):
    db_subdomain = models.Subdomain(subdomain=subdomain.subdomain, domain_id=subdomain.domain_id)
    db.add(db_subdomain)
    db.commit()
    
    db.refresh(db_subdomain)
    return db_subdomain

@router.get("/", response_model=List[schemas.SubdomainResponse])
def read_subdomains(
    domain_id: Optional[uuid.UUID] = None,
    domain_name: Optional[str] = None,
    skill_name_en: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Subdomain).options(joinedload(models.Subdomain.domain))
    if domain_id:
        query = query.filter(models.Subdomain.domain_id == domain_id)
    if domain_name:
        query = query.join(models.Domain).filter(models.Domain.domain.ilike(f"%{domain_name}%"))
    if skill_name_en:
        query = query.join(models.SkillSubdomain).join(models.Skill).filter(models.Skill.skill_name_en.ilike(f"%{skill_name_en}%"))
    subdomains = query.offset(skip).limit(limit).all()
    return subdomains

@router.get("/{subdomain_id}", response_model=schemas.SubdomainResponse)
def read_subdomain(subdomain_id: uuid.UUID, db: Session = Depends(get_db)):
    db_subdomain = db.query(models.Subdomain).options(joinedload(models.Subdomain.domain)).filter(models.Subdomain.id == subdomain_id).first()
    if db_subdomain is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subdomain not found")
    return db_subdomain

@router.put("/{subdomain_id}", response_model=schemas.SubdomainResponse)
def update_subdomain(subdomain_id: uuid.UUID, subdomain: schemas.SubdomainUpdate, db: Session = Depends(get_db)):
    db_subdomain = db.query(models.Subdomain).filter(models.Subdomain.id == subdomain_id).first()
    if db_subdomain is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subdomain not found")
    
    update_data = subdomain.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_subdomain, key, value)
    
    db.add(db_subdomain)
    db.commit()
    db.refresh(db_subdomain)
    return db_subdomain

@router.delete("/{subdomain_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subdomain(subdomain_id: uuid.UUID, db: Session = Depends(get_db)):
    db_subdomain = db.query(models.Subdomain).filter(models.Subdomain.id == subdomain_id).first()
    if db_subdomain is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subdomain not found")
    db.delete(db_subdomain)
    db.commit()
    return {"ok": True}