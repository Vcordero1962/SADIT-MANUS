from src.sadit.clinical.parser import ClinicalParser
from src.sadit.clinical.semiology import SemiologyEngine
from src.sadit.clinical.models import ClinicalInput, LabData
from src.sadit.inference.bayesian import SaditBayesianEngine


def run_simulation():
    print("=== SADIT v1.1.9 CLINICAL SIMULATION ===")
    parser = ClinicalParser()
    sem_engine = SemiologyEngine()
    bayes_engine = SaditBayesianEngine()

    # Test Cases (Raw Text)
    scenarios = [
        {
            "name": "CASE 1 (Mechanical Distal)",
            "text": "Patient reports pain in distal femur towards the knee. Pain is throbbing and worse when walking (load). Surgeon suspects stem tip impact.",
            "ild": 6, "mobility": "independent", "img": "stable"
        },
        {
            "name": "CASE 2 (Mechanical Inguinal/Loosening)",
            "text": "Pain started 3 months after surgery. Located in the groin (inguinal). Patient needs a walker to move. Pain is mechanical.",
            "ild": 3, "mobility": "walker", "img": "loose"
        },
        {
            "name": "CASE 3 (Septic/Osteomyelitic)",
            "text": "Patient complains of deep, boring (terebrante) pain. It wakes them up at night. Constant intensity.",
            "ild": 12, "mobility": "bedridden", "img": "stable"
        }
    ]

    for sc in scenarios:
        print(f"\nProcessing: {sc['name']}")
        print(f" > Input Text: '{sc['text']}'")

        # 1. NLP Parsing
        pp = parser.parse_text_to_profile(sc['text'])
        print(
            f" > Extracted ALICIA: Loc={pp.location}, Char={pp.character}, Night={'night' in pp.aggravating}")

        # 2. Semiology Engine (Safety Score)
        clinical_input = ClinicalInput(
            pain_profile=pp,
            ild_months=sc['ild'],
            mobility_assistance=sc['mobility'],
            lab_data=None
        )
        diag_result = sem_engine.process(clinical_input)
        print(f" > Semiology Diagnosis: {diag_result.diagnosis}")

        # 3. Bayesian Inference
        bayes_res = bayes_engine.infer_diagnosis(
            location=pp.location,
            pain_character=pp.character,
            ild_months=sc['ild'],
            imaging_status=sc['img'],
            mobility=sc['mobility']
        )
        print(
            f" > Bayesian Inference: {bayes_res.most_likely_diagnosis} (P_Infection={bayes_res.infection_prob:.2f})")


if __name__ == "__main__":
    run_simulation()
