from src.core.security import get_password_hash
from src.clinical.models_db import Base as ClinicalBase
from src.core.models import Base as CoreBase, Tenant, User
from src.core.database import engine, SessionLocal
import sys
import os
from sqlalchemy import text
from sqlalchemy.orm import Session

# Add project root to path (using relative path to avoid Windows encoding issues)
sys.path.append(".")


def seed_database():
    print("=== SADIT DATABASE SEEDING START ===")

    db: Session = SessionLocal()
    try:
        # 1. Init Public Tables
        print("[1] Init Public Schema...")
        CoreBase.metadata.create_all(bind=engine)

        # 2. Check/Create Tenant
        tenant_name = "Hospital General Universitario"
        schema_name = "tenant_hospital_general"

        print(f"[2] Checking Tenant {schema_name}...")
        tenant = db.query(Tenant).filter(Tenant.name == tenant_name).first()
        if not tenant:
            tenant = Tenant(name=tenant_name, schema_name=schema_name)
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            print(" -> Tenant Created.")

        # 3. Create Tenant Schema & Tables (ISOLATION STEP)
        print(f"[3] Schema Isolation {schema_name}...")
        with engine.connect() as connection:
            connection.execute(
                text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
            connection.commit()

        ClinicalBase.metadata.schema = schema_name
        ClinicalBase.metadata.create_all(bind=engine)

        # 4. Create Admin User
        user_email = "dr_demo@sadit.com"
        print(f"[4] Checking User {user_email}...")
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            hashed_pwd = get_password_hash("medico123")
            user = User(
                email=user_email,
                hashed_password=hashed_pwd,
                full_name="Dr. Demo User",
                role="doctor",
                tenant_id=tenant.id
            )
            db.add(user)
            db.commit()
            print(" -> User Created.")

        print("=== SEEDING SUCCESS ===")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
