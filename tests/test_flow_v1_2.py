import requests
import sys

BASE_URL = "http://localhost:8000"


def test_full_flow():
    print("=== SADIT v1.2 API FLOW TEST ===")

    # 1. Login
    print("[1] Testing Login (dr_demo@sadit.com)...")
    login_payload = {
        "username": "dr_demo@sadit.com",
        "password": "medico123"
    }
    # FastAPI OAuth2FormRequest expects form-data usually, but let's try
    try:
        r = requests.post(f"{BASE_URL}/auth/login", data=login_payload)
    except Exception as e:
        print(f"FAILED to connect to {BASE_URL}: {e}")
        return

    if r.status_code != 200:
        print(f"FAILED Login: {r.text}")
        return

    token = r.json()["access_token"]
    print(f" -> Login SUCCESS. Token: {token[:10]}...")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Test Case A: High Risk (Septic)
    print("\n[2] Testing High Risk Case (Terebrante/Night Pain)...")
    payload_high = {
        "pain_profile": {
            "onset": "sudden",
            "location": "distal",
            "intensity": 8,
            "character": "terebrante",
            "is_night_pain": True
        },
        "ild_months": 12,
        "mobility": "Independent"
    }

    r_high = requests.post(
        f"{BASE_URL}/inference/clinical", json=payload_high, headers=headers)
    if r_high.status_code == 200:
        data = r_high.json()
        score = data['safetyScore']
        diagnosis = data['diagnosis']
        print(f" -> Response: Score={score}, Diag={diagnosis}")
        if score > 0.4:
            print(" -> PASS: Correctly identified High Risk (>0.4).")
        else:
            print(" -> FAIL: Missed High Risk.")
    else:
        print(f"FAILED Inference: {r_high.status_code} {r_high.text}")

    # 3. Test Case B: Low Risk (Mechanical)
    print("\n[3] Testing Low Risk Case (Mechanical/Gradual)...")
    payload_low = {
        "pain_profile": {
            "onset": "gradual",
            "location": "inguinal",
            "intensity": 4,
            "character": "mechanical",
            "is_night_pain": False
        },
        "ild_months": 36,
        "mobility": "Independent"
    }

    r_low = requests.post(
        f"{BASE_URL}/inference/clinical", json=payload_low, headers=headers)
    if r_low.status_code == 200:
        data = r_low.json()
        score = data['safetyScore']
        diagnosis = data['diagnosis']
        print(f" -> Response: Score={score}, Diag={diagnosis}")
        if score <= 0.4:
            print(" -> PASS: Correctly identified Low Risk (Mechanical).")
        else:
            print(" -> FAIL: False Positive.")
    else:
        print(f"FAILED Inference: {r_low.status_code} {r_low.text}")

    print("\n=== TEST COMPLETE ===")


if __name__ == "__main__":
    test_full_flow()
