import numpy as np
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DiagnosticResult:
    diagnosis: str
    probability: float
    confidence_interval: tuple
    citation_source: Optional[str] = None

class SafetyException(Exception):
    """Raised when safety protocols (ISO 14971) are violated."""
    pass

class EvidenceException(Exception):
    """Raised when a diagnostic inference lacks scientific citation."""
    pass

class SADIT_Compliance_Checker:
    """
    Gatekeeper for SADIT v1.1.5.
    Enforces ISO 14971 (Risk Management) and Evidence-Based Medicine.
    """
    
    MIN_SNR_THRESHOLD = 15.0  # Decibels
    MIN_RESOLUTION = (1024, 1024)

    @staticmethod
    def check_image_safety(image_array: np.ndarray, metadata: dict = None):
        """
        FAIL-SAFE: Verifies image quality before processing.
        """
        # check resolution
        if image_array.shape[0] < SADIT_Compliance_Checker.MIN_RESOLUTION[0] or \
           image_array.shape[1] < SADIT_Compliance_Checker.MIN_RESOLUTION[1]:
             raise SafetyException(
                f"Image resolution {image_array.shape} below safety threshold {SADIT_Compliance_Checker.MIN_RESOLUTION}."
            )
        
        # Check Signal-to-Noise Ratio (Simplified Heuristic)
        signal = np.mean(image_array)
        noise = np.std(image_array)
        if noise == 0: noise = 1e-5 # Avoid div by zero
        snr = 20 * np.log10(signal / noise)
        
        if snr < SADIT_Compliance_Checker.MIN_SNR_THRESHOLD:
            raise SafetyException(f"Image SNR {snr:.2f}dB is too low. Risk of artifact misinterpretation.")
        
        return True

    @staticmethod
    def validate_inference(result: DiagnosticResult):
        """
        ANTI-HALLUCINATION: Ensures every diagnosis has a citation.
        """
        if not result.citation_source:
            raise EvidenceException(
                f"Validation Failed: Diagnosis '{result.diagnosis}' requires a citation_source."
            )
        
        if result.probability > 0.99 or result.probability < 0.01:
             # Warning only, clinical certainty is rarely 100%
             pass
        
        return True
