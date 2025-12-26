from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

from src.sadit.clinical.semiology import SemiologyEngine
from src.sadit.inference.bayesian import SaditBayesianEngine
from src.sadit.clinical.models import ClinicalInput, PainProfile, LabData

from src.api.auth import oauth2_scheme  # Require Auth

router = APIRouter(prefix="/inference", tags=["Clinical Inference"])

# --- Pydantic Models for Input ---


class PainProfileSchema(BaseModel):
    onset: str  # 'sudden', 'gradual'
    location: str  # 'distal', 'inguinal', 'diffuse'
    intensity: int
    character: str  # 'mechanical', 'inflammatory', 'terebrante'
    is_night_pain: bool


class ClinicalAnalysisRequest(BaseModel):
    pain_profile: PainProfileSchema
    ild_months: int = 12  # Default
    mobility: str = "Independent"


# --- Engines Initialization (Singleton scope for simplicity) ---
semiology_engine = SemiologyEngine()
bayesian_engine = SaditBayesianEngine()


@router.post("/clinical")
def analyze_clinical_case(request: ClinicalAnalysisRequest, token: str = Depends(oauth2_scheme)):
    """
    Executes the REAL Inference Pipeline:
    1. Semiology Engine (ALICIA) -> Detects Septic Risk/Safety Score.
    2. Bayesian Engine -> Calculates probability table.
    """
    try:
        # 1. Map Input to Internal Domain Models
        aggravating = []
        if request.pain_profile.is_night_pain:
            aggravating.append('night')

        # ALICIA Input
        pp = PainProfile(
            onset=request.pain_profile.onset,
            location=request.pain_profile.location,
            intensity=request.pain_profile.intensity,
            character=request.pain_profile.character,
            aggravating=aggravating,
            irradiation=False,  # UI doesn't ask yet
            alleviating=[]
        )

        clinical_input = ClinicalInput(
            pain_profile=pp,
            ild_months=request.ild_months,
            mobility_assistance=request.mobility
        )

        # 2. Run Semiology Engine (Rule-Based / Safety)
        sem_result = semiology_engine.process(clinical_input)

        # 3. Run Bayesian Engine (Probabilistic)
        # Using mappings from bayesian.py
        # Heuristic Defaults for missing imaging/ILD context in minimal UI
        bayesian_result = bayesian_engine.infer_diagnosis(
            location=pp.location,
            pain_character=pp.character,
            ild_months=clinical_input.ild_months,
            imaging_status="Stable",  # Default assumption until Vision module connected
            mobility=clinical_input.mobility_assistance
        )

        # 4. Construct Response
        # We prioritize Semiology Alert if Critical (Septic)

        final_diagnosis = sem_result.diagnosis
        final_prob = sem_result.probability

        # Calculate Safety Score explicitly for UI
        safety_score = semiology_engine.calculate_inflammatory_safety_score(pp)

        return {
            "diagnosis": final_diagnosis,
            "probability": final_prob,
            "safetyScore": safety_score,
            "recommendation": "Derivar a Infectología" if safety_score > 0.4 else "Valoración Quirúrgica Estándar",
            "bayesian_details": {
                "impact_prob": bayesian_result.scenario_a_prob,
                "loosening_prob": bayesian_result.scenario_b_prob,
                "infection_prob": bayesian_result.infection_prob,
                "most_likely": bayesian_result.most_likely_diagnosis
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
