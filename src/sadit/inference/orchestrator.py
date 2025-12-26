from ..clinical.models import ClinicalInput, PainProfile
from ..clinical.semiology import SemiologyEngine
from ..physics.materials import MaterialBioMatch
from ..physics.stress import StressCalculator
from ..compliance.checker import SADIT_Compliance_Checker, DiagnosticResult
from .bayesian import SaditBayesianEngine


class SADIT_Orchestrator:
    """
    Master Orchestrator v1.1.9.
    Triangulates Clinical Information (ALICIA), Imaging (Simulated), Physics, AND Bayesian Inference.
    """

    def __init__(self):
        self.clinical = SemiologyEngine()
        self.checker = SADIT_Compliance_Checker
        self.bayesian = SaditBayesianEngine()

    def analyze_case(self,
                     clinical_data: ClinicalInput,
                     implant_type: str,
                     image_array=None,
                     imaging_status: str = "Stable") -> DiagnosticResult:

        # 1. Safety Check (Compliance)
        if image_array is not None:
            self.checker.check_image_safety(image_array)

        # 2. Physics Analysis
        mat_key = "cobalt_chrome" if "austin" in implant_type.lower() else "titanium_alloy"
        mismatch = MaterialBioMatch.calculate_stiffness_mismatch(
            mat_key, "cortical_bone")
        physics_assess = StressCalculator.assess_stress_conditions(
            mismatch, clinical_data.pain_profile.location)

        # 3. Clinical Analysis (Rule-Based ALICIA)
        clinical_result = self.clinical.process(clinical_data)

        # 4. Bayesian Inference (Probabilistic)
        bayes_result = self.bayesian.infer_diagnosis(
            location=clinical_data.pain_profile.location,
            pain_character=clinical_data.pain_profile.character,
            ild_months=clinical_data.ild_months,
            imaging_status=imaging_status,
            mobility=clinical_data.mobility_assistance
        )

        # 5. Synthesis / Triangulation (Final Inference)
        final_diagnosis = f"Bayesian Consensus: {bayes_result.most_likely_diagnosis}"
        final_confidence = max(bayes_result.scenario_a_prob,
                               bayes_result.scenario_b_prob, bayes_result.infection_prob)
        final_citation = f"Bayesian Network v1.1.9 (P={final_confidence:.2f})"

        # Refine diagnosis with physics & rules
        if physics_assess["tip_stress_risk"] == "Critical" and "Scenario_A" in bayes_result.most_likely_diagnosis:
            final_diagnosis += f" | CONFIRMED by Physics: {physics_assess['mechanism']}"
            final_confidence = min(0.99, final_confidence + 0.10)
            final_citation += f" + {physics_assess['citation']}"

        if "Infection" in bayes_result.most_likely_diagnosis:
            final_diagnosis = "CRITICAL: " + final_diagnosis

        # 6. Validation (Anti-Hallucination)
        final_result = DiagnosticResult(
            diagnosis=final_diagnosis,
            probability=final_confidence,
            confidence_interval=(final_confidence - 0.05,
                                 min(1.0, final_confidence + 0.05)),
            citation_source=final_citation
        )

        self.checker.validate_inference(final_result)

        return final_result
