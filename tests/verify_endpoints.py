"""
Social Media Privacy Risk Assessment Framework
End-to-End API & Frontend Endpoint Verification Script
"""

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.app import create_app

def verify_all():
    print("[*] Initializing Flask test client for full stack verification...")
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    routes_to_test = [
        ("/", 200, "Frontend Home"),
        ("/assessment", 200, "Frontend Assessment Wizard"),
        ("/dashboard", 200, "Frontend Dashboard"),
        ("/simulator", 200, "Frontend Simulator"),
        ("/metadata", 200, "Frontend Metadata Inspector"),
        ("/report", 200, "Frontend Report Template"),
        ("/css/styles.css", 200, "CSS Stylesheet"),
        ("/js/app.js", 200, "JS App"),
        ("/js/assessment.js", 200, "JS Assessment"),
        ("/js/dashboard.js", 200, "JS Dashboard"),
        ("/js/simulator.js", 200, "JS Simulator"),
        ("/api/health", 200, "API Health"),
        ("/api/questionnaire", 200, "API Questionnaire"),
        ("/api/dashboard/stats", 200, "API Dashboard Stats"),
        ("/api/privacy-checklist", 200, "API Privacy Checklist")
    ]

    all_passed = True
    for route, expected_status, label in routes_to_test:
        res = client.get(route)
        if res.status_code == expected_status:
            print(f"  [PASS] {label:<32} -> {route} ({res.status_code})")
        else:
            print(f"  [FAIL] {label:<32} -> {route} (Expected {expected_status}, got {res.status_code})")
            all_passed = False

    # Test Assessment Submission & Score Calculation
    sample_payload = {
        "responses": {
            "q1": "PUBLIC",
            "q5": "YES",
            "q10": "YES",
            "q27": "DISABLED"
        }
    }
    post_res = client.post("/api/assessment", json=sample_payload)
    if post_res.status_code == 201:
        data = post_res.get_json()
        print(f"\n  [PASS] API Assessment Submission -> ID: {data['assessment_id']}, Score: {data['overall_score']}, Tier: {data['risk_level']}")
    else:
        print(f"\n  [FAIL] API Assessment Submission failed: {post_res.status_code}")
        all_passed = False

    if all_passed:
        print("\n[+] ALL ENDPOINTS & FRONTEND ASSETS VERIFIED SUCCESSFULLY!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    verify_all()
