from sadit.clinical.semiology import ClinicalInput, LabData
from sadit.inference.orchestrator import SADIT_Orchestrator
import sys
import os
import numpy as np

# Add src to path for import
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


def run_simulation():
    print("=== SADIT v1.1.5 Simulation: Austin-Moore Case ===")

    # Initialize Orchestrator
    orchestrator = SADIT_Orchestrator()

    # CASE DATA: Patient with Austin-Moore, Distal Pain, No Infection (Normal labs)
    # Scenario A: Distal Impact
    patient_data = ClinicalInput(
        pain_location='distal',
        pain_onset_months=1,
        ild_months=0,  # Immediate pain (bad sign for integration)
        mobility_assistance='cane',
        # Normal Hitachi Cobas C3 values
        lab_data=LabData(pcr_level=0.1, vsg_level=10, wbc_count=7000)
    )

    implant = "Austin-Moore Hemiarthroplasty"

    # Create Dummy Image (Safe)
    dummy_image = np.ones((2000, 2000)) * 100  # Good resolution, uniform

    print(f"Patient Input: {patient_data}")
    print(f"Implant: {implant}")

    try:
        result = orchestrator.analyze_case(patient_data, implant, dummy_image)

        print("\n=== DIAGNOSTIC OUTPUT ===")
        print(f"Diagnosis: {result.diagnosis}")
        print(f"Probability: {result.probability:.2f}")
        print(f"Confidence Interval: {result.confidence_interval}")
        print(f"Evidence Base: {result.citation_source}")

        if "Physics" in result.diagnosis:
            print("\n[SUCCESS] System correctly identified Physics correlation.")
        else:
            print("\n[WARNING] Physics correlation possibly missed.")

    except Exception as e:
        print(f"Simulation Failed: {e}")


if __name__ == "__main__":
    run_simulation()
