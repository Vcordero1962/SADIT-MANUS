from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base


class Tenant(Base):
    """
    Represents an Institution (Hospital/Clinic).
    Lives in the 'public' schema.
    """
    __tablename__ = "tenants"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    # e.g., 'hospital_a_schema'
    schema_name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    """
    Represents a Professional (Doctor/Researcher).
    Global user living in 'public', associated with a Tenant.
    """
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    # 'doctor', 'researcher', 'student'
    role = Column(String, default="doctor")

    tenant_id = Column(Integer, ForeignKey("public.tenants.id"))
    is_active = Column(Boolean, default=True)
