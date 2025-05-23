import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from .models import SkillType

# Base Schemas

class DomainBase(BaseModel):
    domain: str

class SubdomainBase(BaseModel):
    subdomain: str
    domain_id: uuid.UUID

class SkillBase(BaseModel):
    skill_name_en: str
    skill_name_jp: Optional[str] = None
    skill_type: SkillType
    synonyms_en: List[str] = Field(default_factory=list)
    synonyms_jp: List[str] = Field(default_factory=list)

class JobTitleBase(BaseModel):
    job_title: str
    synonyms_en: List[str] = Field(default_factory=list)
    synonyms_jp: List[str] = Field(default_factory=list)

# Create Schemas

class DomainCreate(DomainBase):
    pass

class SubdomainCreate(SubdomainBase):
    pass

class SkillCreate(SkillBase):
    pass

class JobTitleCreate(JobTitleBase):
    pass

# Update Schemas

class DomainUpdate(DomainBase):
    domain: Optional[str] = None

class SubdomainUpdate(SubdomainBase):
    subdomain: Optional[str] = None
    domain_id: Optional[uuid.UUID] = None

class SkillUpdate(SkillBase):
    skill_name_en: Optional[str] = None
    skill_name_jp: Optional[str] = None
    skill_type: Optional[SkillType] = None
    synonyms_en: List[str] = Field(default_factory=list)
    synonyms_jp: List[str] = Field(default_factory=list)

class JobTitleUpdate(JobTitleBase):
    job_title: Optional[str] = None
    synonyms_en: Optional[List[str]] = None
    synonyms_jp: Optional[List[str]] = None

# Response Schemas

class DomainResponse(DomainBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class SubdomainResponse(SubdomainBase):
    id: uuid.UUID
    domain: DomainResponse

    class Config:
        from_attributes = True

class SkillResponse(SkillBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class JobTitleResponse(JobTitleBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

# Join Table Schemas (for relationships)

class SkillSubdomainLink(BaseModel):
    skill_id: uuid.UUID
    subdomain_id: uuid.UUID

    class Config:
        from_attributes = True

class JobTitleCoreSkillLink(BaseModel):
    job_title_id: uuid.UUID
    skill_id: uuid.UUID

    class Config:
        from_attributes = True

class JobTitleSubdomainLink(BaseModel):
    job_title_id: uuid.UUID
    subdomain_id: uuid.UUID

    class Config:
        from_attributes = True

# Nested Response Schemas for relationships

class SubdomainWithSkills(SubdomainResponse):
    skills: List[SkillResponse] = []

class SkillWithSubdomains(SkillResponse):
    subdomains: List[SubdomainResponse] = []

class JobTitleWithSkills(JobTitleResponse):
    core_skills: List[SkillResponse] = []

class JobTitleWithSubdomains(JobTitleResponse):
    subdomains: List[SubdomainResponse] = []