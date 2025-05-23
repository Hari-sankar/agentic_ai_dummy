import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base
import enum

class SkillType(enum.Enum):
    soft = "soft"
    technical = "technical"
    other = "other"

class Domain(Base):
    __tablename__ = "domain"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain = Column(String, nullable=False)
    subdomains = relationship("Subdomain", back_populates="domain")

class Subdomain(Base):
    __tablename__ = "subdomain"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subdomain = Column(String, nullable=False)
    domain_id = Column(UUID(as_uuid=True), ForeignKey("domain.id", ondelete="CASCADE"), nullable=False)
    domain = relationship("Domain", back_populates="subdomains")
    skills = relationship("SkillSubdomain", back_populates="subdomain")
    job_titles = relationship("JobTitleSubdomain", back_populates="subdomain")

class Skill(Base):
    __tablename__ = "skill"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_name_en = Column(String, nullable=False)
    skill_name_jp = Column(String)
    skill_type = Column(Enum(SkillType), nullable=False)
    synonyms_en = Column(ARRAY(String))
    synonyms_jp = Column(ARRAY(String))
    subdomains = relationship("SkillSubdomain", back_populates="skill")
    job_titles = relationship("JobTitleCoreSkill", back_populates="skill")

class JobTitle(Base):
    __tablename__ = "job_title"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_title = Column(String, nullable=False)
    synonyms_en = Column(ARRAY(String))
    synonyms_jp = Column(ARRAY(String))
    core_skills = relationship("JobTitleCoreSkill", back_populates="job_title")
    subdomains = relationship("JobTitleSubdomain", back_populates="job_title")

class SkillSubdomain(Base):
    __tablename__ = "skill_subdomain"
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skill.id", ondelete="CASCADE"), primary_key=True)
    subdomain_id = Column(UUID(as_uuid=True), ForeignKey("subdomain.id", ondelete="CASCADE"), primary_key=True)
    skill = relationship("Skill", back_populates="subdomains")
    subdomain = relationship("Subdomain", back_populates="skills")

class JobTitleCoreSkill(Base):
    __tablename__ = "job_title_core_skill"
    job_title_id = Column(UUID(as_uuid=True), ForeignKey("job_title.id", ondelete="CASCADE"), primary_key=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skill.id", ondelete="CASCADE"), primary_key=True)
    job_title = relationship("JobTitle", back_populates="core_skills")
    skill = relationship("Skill", back_populates="job_titles")

class JobTitleSubdomain(Base):
    __tablename__ = "job_title_subdomain"
    job_title_id = Column(UUID(as_uuid=True), ForeignKey("job_title.id", ondelete="CASCADE"), primary_key=True)
    subdomain_id = Column(UUID(as_uuid=True), ForeignKey("subdomain.id", ondelete="CASCADE"), primary_key=True)
    job_title = relationship("JobTitle", back_populates="subdomains")
    subdomain = relationship("Subdomain", back_populates="job_titles")