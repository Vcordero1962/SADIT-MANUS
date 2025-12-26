from .models import ClinicalInput, PainProfile
from ..compliance.checker import DiagnosticResult


class SemiologyEngine:
    """
    Advanced Semiology Engine (SADIT v1.1.9)
    Uses ALICIA protocol to distinguish Mechanical vs Inflammatory patterns.
    """

    def calculate_inflammatory_safety_score(self, pp: PainProfile) -> float:
        """
        Calculates a safety score (0.0 to 1.0).
        High Score (>0.4) = High Risk of Infection/Inflammation.
        """
        score = 0.0
        if pp.character in ['inflammatory', 'terebrante', 'boring']:
            score += 0.6
        if 'night' in pp.aggravating:
            score += 0.3
        if 'rest' not in pp.alleviating:  # Pain at rest
            score += 0.2
        return min(score, 1.0)

    def process(self, data: ClinicalInput) -> DiagnosticResult:
        pp = data.pain_profile

        # 1. Safety Filter: Inflammatory Safety Score (ISS)
        inflam_score = self.calculate_inflammatory_safety_score(pp)
        is_septic_risk = inflam_score > 0.4

        infection_ruled_out = False
        if data.lab_data:
            # Simplified infection screening: Low PCR and VSG rules out infection
            if data.lab_data.pcr_level and data.lab_data.vsg_level:
                if data.lab_data.pcr_level < 10.0 and data.lab_data.vsg_level < 20:
                    infection_ruled_out = True

        # PRIORITY 1: Infection Rule Out
        if is_septic_risk and not infection_ruled_out:
            diagnosis_msg = "WARNING: Inflammatory Pain Profile."
            if pp.character in ['terebrante', 'boring', 'taladrante']:
                diagnosis_msg = "CRITICAL: Deep Bone Pain (Osteomyelitic Origin). Suspected Septic Process."

            return DiagnosticResult(
                diagnosis=f"{diagnosis_msg} (ISS: {inflam_score:.2f})",
                probability=0.85 +
                (0.1 if pp.character in ['terebrante', 'taladrante'] else 0),
                confidence_interval=(0.80, 0.95),
                citation_source="ALICIA: Inflammatory/Terebrante markers require ruling out PJI."
            )

        # PRIORITY 1.5: Osteomyelitic Specific (Septic Origin)
        if pp.character in ['terebrante', 'boring', 'taladrante']:
            return DiagnosticResult(
                diagnosis="CRITICAL: Deep Bone Pain (Osteomyelitic Origin). Suspected Septic Process.",
                probability=0.92,
                confidence_interval=(0.88, 0.95),
                citation_source="Semiology: 'Terebrante' character indicates intra-osseous pressure/Infection."
            )

        # 2. Chronopathology & Mechanics
        if pp.location == 'inguinal' and pp.character == 'mechanical':
            # Typical Loosening
            return DiagnosticResult(
                diagnosis="Probable Aseptic Loosening (Scenario B)",
                probability=0.88,
                confidence_interval=(0.85, 0.92),
                citation_source=f"Inguinal Mechanical Pain + ILD {data.ild_months}mo"
            )

        if pp.location == 'distal' and pp.character == 'mechanical':
            # Typical Structural Mismatch (Stem Tip Pain)
            return DiagnosticResult(
                diagnosis="Potential Material Stiffness Mismatch (Scenario A)",
                probability=0.85,
                confidence_interval=(0.80, 0.90),
                citation_source="Distal Pain + Mechanical Pattern (Wolff's Law)"
            )

        # Default / Mixed
        return DiagnosticResult(
            diagnosis="Undetermined Mechanical Etiology. Correlate with Imaging.",
            probability=0.50,
            confidence_interval=(0.40, 0.60),
            citation_source="Clinical features inconclusive."
        )
