from sadit.inference.bayesian import SaditBayesianEngine
from sadit.clinical.models import ClinicalInput, PainProfile
from sadit.clinical.semiology import SemiologyEngine
import sys
import os

# Ensure src is in path
sys.path.append(os.path.abspath("src"))


def print_heat_map(case_name, zone_conflict, prob_map):
    print(f"\n>> MAPA DE CALOR DE PROBABILIDAD: {case_name}")
    print(f"   [ ZONA DE CONFLICTO MECÁNICO: {zone_conflict} ]")
    print("   ------------------------------------------------")
    print(f"   | Proximal (Inguinal) | {prob_map.get('proximal', 0.0):.2f}")
    print(f"   |---------------------|")
    print(f"   | Distal   (Thigh)    | {prob_map.get('distal', 0.0):.2f}")
    print(f"   |---------------------|")
    print(f"   | Septic   (Diff/Deep)| {prob_map.get('septic', 0.0):.2f}")
    print("   ------------------------------------------------")


def run_stress_audit():
    print("=== AUDITORÍA DE STRESS-ZONES (SADIT v1.1.9) ===")
    sem = SemiologyEngine()
    bayes = SaditBayesianEngine()

    # --- TEST A: Case 1 (Distal Impact) ---
    print("\n[PRUEBA A] Escenario Distal (Caso 1: WhatsApp Images)")
    # Input Simulation based on file analysis
    pp_a = PainProfile(onset='gradual', location='distal', intensity=7, character='mechanical',
                       aggravating=['load'], alleviating=['rest'], irradiation=False)

    # Bayesian Inference
    res_a = bayes.infer_diagnosis(location='Distal', pain_character='Mechanical',
                                  ild_months=6, imaging_status='Stable', mobility='Independent')

    # Logic Validation
    print(f" > Diagnóstico Inferido: {res_a.most_likely_diagnosis}")
    print(f" > Confianza (Impacto): {res_a.scenario_a_prob:.4f}")

    # Heat Map Data
    probs_a = {'proximal': res_a.scenario_b_prob,
               'distal': res_a.scenario_a_prob, 'septic': res_a.infection_prob}
    print_heat_map("Caso 1 (Vástago Rígido)",
                   "TERCIO DISTAL (Wolff's Law Stress)", probs_a)

    # --- TEST B: Case 2 (Proximal Loosening) ---
    print("\n[PRUEBA B] Escenario Proximal (Caso 2: Segundo Caso + Audio 71yo)")
    # Input Simulation
    pp_b = PainProfile(onset='gradual', location='inguinal', intensity=8, character='mechanical',
                       aggravating=['load'], alleviating=['rest'], irradiation=False)

    # Bayesian Inference (Late Onset, Assisted Mobility)
    res_b = bayes.infer_diagnosis(location='Inguinal', pain_character='Mechanical',
                                  ild_months=3, imaging_status='Loose', mobility='Assisted')

    print(f" > Diagnóstico Inferido: {res_b.most_likely_diagnosis}")
    print(f" > Confianza (Aflojamiento): {res_b.scenario_b_prob:.4f}")

    probs_b = {'proximal': res_b.scenario_b_prob,
               'distal': res_b.scenario_a_prob, 'septic': res_b.infection_prob}
    print_heat_map("Caso 2 (Micro-movimiento)",
                   "ZONA DE GRUEN 1/7 (Proximal)", probs_b)

    # --- TEST C: Septic Discrimination (Stress Injection) ---
    print("\n[PRUEBA C] Discriminación Séptica (Inyección de Variable 'Terebrante')")
    print(" > INJECTING: character='terebrante' into Case 2 Context...")

    pp_c = PainProfile(onset='gradual', location='inguinal', intensity=9, character='terebrante',
                       aggravating=['night', 'load'], alleviating=[], irradiation=False)

    # Semiology Check
    safety_score = sem.calculate_inflammatory_safety_score(pp_c)
    print(f" > SafetyScore Calculado: {safety_score:.2f}")

    diag_c = sem.process(ClinicalInput(
        pain_profile=pp_c, ild_months=3, mobility_assistance="Assisted"))
    print(f" > Semiology Output: {diag_c.diagnosis}")

    if safety_score > 0.4 and "CRITICAL" in diag_c.diagnosis:
        print(" > RESULTADO DE STRESS: PASS (Alerta Activada Correctamente)")
    else:
        print(" > RESULTADO DE STRESS: FAIL")


if __name__ == "__main__":
    run_stress_audit()
