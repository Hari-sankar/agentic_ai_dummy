from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
import uuid

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/job_titles",
    tags=["Job Titles"]
)

@router.post("/", response_model=schemas.JobTitleResponse, status_code=status.HTTP_201_CREATED)
def create_job_title(job_title: schemas.JobTitleCreate, db: Session = Depends(get_db)):
    db_job_title = models.JobTitle(**job_title.model_dump())
    db.add(db_job_title)
    db.commit()
    db.refresh(db_job_title)
    return db_job_title

@router.get("/", response_model=List[schemas.JobTitleResponse])
def read_job_titles(
    skill_id: Optional[uuid.UUID] = None,
    skill_name_en: Optional[str] = None,
    skill_type: Optional[models.SkillType] = None,
    subdomain_id: Optional[uuid.UUID] = None,
    subdomain_name: Optional[str] = None,
    domain_id: Optional[uuid.UUID] = None,
    domain_name: Optional[str] = None,
    synonym_en: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.JobTitle)

    if skill_id:
        query = query.join(models.JobTitleCoreSkill).filter(models.JobTitleCoreSkill.skill_id == skill_id)
    if skill_name_en:
        query = query.join(models.JobTitleCoreSkill).join(models.Skill).filter(models.Skill.skill_name_en.ilike(f"%{skill_name_en}%"))
    if skill_type:
        query = query.join(models.JobTitleCoreSkill).join(models.Skill).filter(models.Skill.skill_type == skill_type)
    if subdomain_id:
        query = query.join(models.JobTitleSubdomain).filter(models.JobTitleSubdomain.subdomain_id == subdomain_id)
    if subdomain_name:
        query = query.join(models.JobTitleSubdomain).join(models.Subdomain).filter(models.Subdomain.subdomain.ilike(f"%{subdomain_name}%"))
    if domain_id:
        query = query.join(models.JobTitleSubdomain).join(models.Subdomain).filter(models.Subdomain.domain_id == domain_id)
    if domain_name:
        query = query.join(models.JobTitleSubdomain).join(models.Subdomain).join(models.Domain).filter(models.Domain.domain.ilike(f"%{domain_name}%"))
    if synonym_en:
        query = query.filter(models.JobTitle.synonyms_en.contains([synonym_en]))

    job_titles = query.offset(skip).limit(limit).all()
    return job_titles

@router.get("/{job_title_id}", response_model=schemas.JobTitleResponse)
def read_job_title(job_title_id: uuid.UUID, db: Session = Depends(get_db)):
    db_job_title = db.query(models.JobTitle).filter(models.JobTitle.id == job_title_id).first()
    if db_job_title is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job Title not found")
    return db_job_title

@router.put("/{job_title_id}", response_model=schemas.JobTitleResponse)
def update_job_title(job_title_id: uuid.UUID, job_title: schemas.JobTitleUpdate, db: Session = Depends(get_db)):
    db_job_title = db.query(models.JobTitle).filter(models.JobTitle.id == job_title_id).first()
    if db_job_title is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job Title not found")
    
    update_data = job_title.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job_title, key, value)
    
    db.add(db_job_title)
    db.commit()
    db.refresh(db_job_title)
    return db_job_title

@router.delete("/{job_title_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_title(job_title_id: uuid.UUID, db: Session = Depends(get_db)):
    db_job_title = db.query(models.JobTitle).filter(models.JobTitle.id == job_title_id).first()
    if db_job_title is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job Title not found")
    db.delete(db_job_title)
    db.commit()
    return {"ok": True}