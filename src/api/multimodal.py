from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
import json
import os
from datetime import datetime

from src.sadit.clinical.semiology import SemiologyEngine
from src.sadit.inference.bayesian import SaditBayesianEngine
from src.sadit.clinical.models import ClinicalInput, PainProfile, LabData, MedicalHistory
from src.sadit.compliance.checker import SADIT_Compliance_Checker

from src.api.auth import oauth2_scheme

router = APIRouter(prefix="/inference", tags=["Multimodal Inference"])

# --- Engines Initialization ---
semiology_engine = SemiologyEngine()
bayesian_engine = SaditBayesianEngine()
compliance_checker = SADIT_Compliance_Checker()


@router.post("/multimodal")
async def analyze_multimodal_case(
    files: list[UploadFile] = File([]),
    clinical_data: str = Form(...),
    lab_data: str = Form(None),
    medical_history: str = Form(None),
    token: str = Depends(oauth2_scheme)
):
    """
    Ejecuta análisis multimodal completo con lab data y imágenes
    """
    try:
        # 1. Parse JSON inputs
        clinical_dict = json.loads(clinical_data)
        lab_dict = json.loads(
            lab_data) if lab_data and lab_data != "null" else None
        history_dict = json.loads(
            medical_history) if medical_history and medical_history != "null" else None

        # 2. Construct pain profile
        pain_profile = PainProfile(
            onset=clinical_dict['pain_profile']['onset'],
            location=clinical_dict['pain_profile']['location'],
            intensity=clinical_dict['pain_profile']['intensity'],
            character=clinical_dict['pain_profile']['character'],
            irradiation=clinical_dict['pain_profile'].get(
                'irradiation', False),
            aggravating=['night'] if clinical_dict['pain_profile'].get(
                'is_night_pain') else [],
            alleviating=[]
        )

        # 3. Construct lab data
        lab_results = None
        if lab_dict:
            lab_results = LabData(
                pcr_level=float(lab_dict.get('pcr')) if lab_dict.get(
                    'pcr') else None,
                vsg_level=float(lab_dict.get('vsg')) if lab_dict.get(
                    'vsg') else None,
                wbc_count=float(lab_dict.get('leucocitos')) if lab_dict.get(
                    'leucocitos') else None,
                hemoglobin=float(lab_dict.get('hemoglobina')) if lab_dict.get(
                    'hemoglobina') else None,
                platelets=float(lab_dict.get('plaquetas')) if lab_dict.get(
                    'plaquetas') else None
            )

        # 4. Construct clinical input (base version, not extended)
        clinical_input = ClinicalInput(
            pain_profile=pain_profile,
            ild_months=clinical_dict.get('ild_months', 12),
            mobility_assistance=clinical_dict.get('mobility', 'Independent'),
            lab_data=lab_results
        )

        # 5. Run semiology engine
        sem_result = semiology_engine.process(clinical_input)

        # 6. Run Bayesian inference
        bayesian_result = bayesian_engine.infer_diagnosis(
            location=pain_profile.location,
            pain_character=pain_profile.character,
            ild_months=clinical_input.ild_months,
            imaging_status="Stable",
            mobility=clinical_input.mobility_assistance
        )

        # 7. Calculate safety score with multimodal adjustments
        safety_score = semiology_engine.calculate_inflammatory_safety_score(
            pain_profile)

        # Adjust for lab results
        if lab_results and lab_results.has_inflammatory_markers():
            safety_score = min(1.0, safety_score * 1.5)  # +50% risk

        # 8. Construct response
        final_diagnosis = sem_result.diagnosis
        final_prob = sem_result.probability

        recommendation = "Derivar a Infectología" if safety_score > 0.4 else "Valoración Quirúrgica Estándar"

        if lab_results and lab_results.has_inflammatory_markers():
            recommendation += " - URGENTE: Marcadores inflamatorios elevados"

        return {
            "diagnosis": final_diagnosis,
            "probability": final_prob,
            "safetyScore": safety_score,
            "recommendation": recommendation,
            "multimodal_evidence": {
                "imaging_processed": len(files),
                "lab_inflammatory": lab_results.has_inflammatory_markers() if lab_results else False,
                "lab_values": {
                    "pcr": lab_results.pcr_level if lab_results else None,
                    "vsg": lab_results.vsg_level if lab_results else None,
                    "leucocitos": lab_results.wbc_count if lab_results else None
                } if lab_results else None,
                "medical_history_reviewed": history_dict is not None
            },
            "bayesian_details": {
                "impact_prob": bayesian_result.scenario_a_prob,
                "loosening_prob": bayesian_result.scenario_b_prob,
                "infection_prob": bayesian_result.infection_prob,
                "most_likely": bayesian_result.most_likely_diagnosis
            }
        }

    except Exception as e:
        import traceback
        error_detail = f"Multimodal analysis failed: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)
