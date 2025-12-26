from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.database import engine
from src.core import models as core_models
from src.api.auth import router as auth_router
from src.api.inference import router as inference_router
from src.api.multimodal import router as multimodal_router

# Initialize Public Tables (Tenants/Users) on Startup
core_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SADIT v1.1.9 API (Medical Multi-Tenant)",
    description="Backend API for SADIT utilizing Schema Isolation.",
    version="1.3.0"
)

app.include_router(auth_router)
app.include_router(inference_router)
app.include_router(multimodal_router)

# CORS Configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "online", "system": "SADIT v1.2", "mode": "Multi-Tenant (Schema Isolation)"}


@app.get("/health")
def health_check():
    return {"db_status": "configured", "inference_engine": "loaded"}
