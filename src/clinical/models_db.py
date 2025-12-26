from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# Separate Base for dynamic schemas might be needed,
# but for definition we use a mixin or abstract base if not bound immediately.
# For now, we define them but they will be created in specific schemas dynamically.

from src.core.database import Base


class Patient(Base):
    """
    Patient Data Subject.
    Isolated per Tenant Schema.
    """
    __tablename__ = "patients"
    # No __table_args__ schema here; assigned dynamically at runtime or migration

    id = Column(Integer, primary_key=True, index=True)
    medical_record_number = Column(String, index=True, nullable=False)
    full_name = Column(String)
    age = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MedicalRecord(Base):
    """
    Longitudinal Health Record (HCL).
    Isolated per Tenant Schema.
    """
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))

    # ALICIA Protocol Data
    # Stores onset, location, character (Terebrante), etc.
    pain_profile_json = Column(JSON)
    safety_score = Column(Float)

    # Diagnosis
    inferred_diagnosis = Column(String)
    confidence = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
