from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
import uuid

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)

@router.post("/", response_model=schemas.SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(skill: schemas.SkillCreate, db: Session = Depends(get_db)):
    db_skill = models.Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.get("/", response_model=List[schemas.SkillResponse])
def read_skills(
    skill_type: Optional[models.SkillType] = None,
    subdomain_id: Optional[uuid.UUID] = None,
    subdomain_name: Optional[str] = None,
    domain_id: Optional[uuid.UUID] = None,
    domain_name: Optional[str] = None,
    synonym_en: Optional[str] = None,
    job_title_id: Optional[uuid.UUID] = None,
    job_title_name: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Skill)
    
    if skill_type:
        query = query.filter(models.Skill.skill_type == skill_type)
    if subdomain_id:
        query = query.join(models.SkillSubdomain).filter(models.SkillSubdomain.subdomain_id == subdomain_id)
    if subdomain_name:
        query = query.join(models.SkillSubdomain).join(models.Subdomain).filter(models.Subdomain.subdomain.ilike(f"%{subdomain_name}%"))
    if domain_id:
        query = query.join(models.SkillSubdomain).join(models.Subdomain).filter(models.Subdomain.domain_id == domain_id)
    if domain_name:
        query = query.join(models.SkillSubdomain).join(models.Subdomain).join(models.Domain).filter(models.Domain.domain.ilike(f"%{domain_name}%"))
    if synonym_en:
        query = query.filter(models.Skill.synonyms_en.contains([synonym_en]))
    if job_title_id:
        query = query.join(models.JobTitleCoreSkill).filter(models.JobTitleCoreSkill.job_title_id == job_title_id)
    if job_title_name:
        query = query.join(models.JobTitleCoreSkill).join(models.JobTitle).filter(models.JobTitle.job_title.ilike(f"%{job_title_name}%"))

    skills = query.offset(skip).limit(limit).all()
    return skills

@router.get("/{skill_id}", response_model=schemas.SkillResponse)
def read_skill(skill_id: uuid.UUID, db: Session = Depends(get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if db_skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return db_skill

@router.put("/{skill_id}", response_model=schemas.SkillResponse)
def update_skill(skill_id: uuid.UUID, skill: schemas.SkillUpdate, db: Session = Depends(get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if db_skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    
    update_data = skill.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_skill, key, value)
    
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(skill_id: uuid.UUID, db: Session = Depends(get_db)):
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if db_skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    db.delete(db_skill)
    db.commit()
    return {"ok": True}