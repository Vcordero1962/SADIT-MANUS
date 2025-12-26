from sadit.inference.bayesian import SaditBayesianEngine
import sys
import os
import pytest

# Add src to path
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../src')))


def test_bayesian_scenarios():
    print("\n=== SADIT v1.1.8: Bayesian Engine Verification ===")
    engine = SaditBayesianEngine()

    # CASE 1: Classic Distal Impact (Scenario A)
    # Distal Pain, Short ILD, Stable Image, Independent Mobility
    print("\n[TEST] Processing Case 1 (Distal/Short/Stable)...")
    result_a = engine.infer_diagnosis(
        location="distal",
        ild_months=1,
        imaging_status="Stable",
        mobility="none"
    )

    print(f"   -> Result: {result_a.most_likely_diagnosis}")
    print(f"   -> P(Scenario_A): {result_a.scenario_a_prob:.4f}")
    print(f"   -> P(Scenario_B): {result_a.scenario_b_prob:.4f}")

    if result_a.scenario_a_prob > 0.8:
        print("   [PASS] Correctly identified Scenario A with high confidence.")
    else:
        print("   [FAIL] Confidence too low for Scenario A.")

    # CASE 2: Aseptic Loosening (Scenario B)
    # Inguinal Pain, Long ILD (>2mo), Loose Image, Assisted Mobility
    print("\n[TEST] Processing Case 2 (Inguinal/Long/Loose)...")
    result_b = engine.infer_diagnosis(
        location="inguinal",
        ild_months=6,
        imaging_status="Radiolucent Line",
        mobility="cane"
    )

    print(f"   -> Result: {result_b.most_likely_diagnosis}")
    print(f"   -> P(Scenario_A): {result_b.scenario_a_prob:.4f}")
    print(f"   -> P(Scenario_B): {result_b.scenario_b_prob:.4f}")

    if result_b.scenario_b_prob > 0.8:
        print("   [PASS] Correctly identified Scenario B with high confidence.")
    else:
        print("   [FAIL] Confidence too low for Scenario B.")


if __name__ == "__main__":
    test_bayesian_scenarios()
