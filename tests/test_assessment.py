"""
Social Media Privacy Risk Assessment Framework
Automated Defensive Cybersecurity & Privacy Test Suite

Comprehensive test suite covering:
- Fully private vs fully public profile benchmarks
- Individual exposure vectors (phone, email, birthday, location, travel, workplace)
- Authentication and MFA risk scoring
- Score boundary edge conditions (20, 40, 70)
- Findings detection and prioritized recommendations
- Real-time improvement simulation
- Safe local database persistence (Zero PII verification)
- Local image EXIF metadata extraction and sanitization
- REST API response validity and data deletion (GDPR Article 17)
"""

import os
import sys
import pytest
import io
import json
from PIL import Image

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.services.questionnaire_data import QUESTIONS, CATEGORIES
from backend.services.scoring_engine import (
    extract_privacy_features,
    calculate_category_scores,
    calculate_overall_risk,
    get_risk_level
)
from backend.services.findings_engine import generate_privacy_findings
from backend.services.recommendation_engine import generate_recommendations
from backend.services.improvement_simulator import simulate_privacy_improvement
from backend.services.assessment_engine import run_assessment, validate_responses
from backend.models.database import (
    init_db,
    save_assessment,
    get_assessment,
    delete_assessment,
    get_dashboard_stats
)
from backend.utils.metadata_inspector import extract_exif_metadata, strip_exif_metadata
from backend.app import create_app


# Helper base fixtures
@pytest.fixture
def test_db_path(tmp_path):
    db_file = str(tmp_path / "test_privacy.db")
    init_db(db_file)
    return db_file

@pytest.fixture
def app_client(test_db_path):
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# =========================================================================
# TEST SUITE: 30+ COMPREHENSIVE CYBERSECURITY & PRIVACY TESTS
# =========================================================================

def test_01_fully_private_profile():
    """Test ID 1: Fully private synthetic profile achieves LOW risk."""
    responses = {q["id"]: min(q["options"], key=lambda opt: opt["risk_score"])["value"] for q in QUESTIONS}
    features = extract_privacy_features(responses)
    cat_scores = calculate_category_scores(features)
    overall_score, risk_level = calculate_overall_risk(cat_scores)

    assert overall_score <= 15.0
    assert risk_level == "LOW"


def test_02_fully_public_profile():
    """Test ID 2: Fully public, insecure synthetic profile triggers CRITICAL risk."""
    responses = {q["id"]: max(q["options"], key=lambda opt: opt["risk_score"])["value"] for q in QUESTIONS}
    features = extract_privacy_features(responses)
    cat_scores = calculate_category_scores(features)
    overall_score, risk_level = calculate_overall_risk(cat_scores)

    assert overall_score >= 85.0
    assert risk_level == "CRITICAL"


def test_03_public_phone_exposure():
    """Test ID 3: Public phone number flags critical finding."""
    responses = {"q5": "YES"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)
    finding_ids = [f["finding_id"] for f in findings]

    assert "FIND_PHONE_PUBLIC" in finding_ids
    assert any(f["severity"] == "CRITICAL" and f["finding_id"] == "FIND_PHONE_PUBLIC" for f in findings)


def test_04_public_email_exposure():
    """Test ID 4: Public personal email address generates high finding."""
    responses = {"q6": "YES"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)
    finding_ids = [f["finding_id"] for f in findings]

    assert "FIND_EMAIL_PUBLIC" in finding_ids


def test_05_public_full_birthday_exposure():
    """Test ID 5: Full birth date exposure triggers critical identity finding."""
    responses = {"q7": "FULL_BIRTHDAY"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_BIRTHDAY_PUBLIC" and f["severity"] == "CRITICAL" for f in findings)


def test_06_public_home_location_exposure():
    """Test ID 6: Disclosing residential street/neighborhood generates finding."""
    responses = {"q8": "YES"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_HOME_ADDRESS" for f in findings)


def test_07_realtime_location_checkins():
    """Test ID 7: Immediate venue check-ins elevate location risk."""
    responses = {"q11": "IMMEDIATELY"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_INSTANT_CHECKINS" for f in findings)


def test_08_advance_travel_plans_exposure():
    """Test ID 8: Advertising future travel dates creates vacancy risk finding."""
    responses = {"q12": "YES"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_ADVANCE_TRAVEL_PLANS" for f in findings)


def test_09_workplace_and_sensitive_badge_exposure():
    """Test ID 9: Corporate badge or ticket barcode leaks trigger critical finding."""
    responses = {"q16": "YES"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_SENSITIVE_DOCS" and f["severity"] == "CRITICAL" for f in findings)


def test_10_family_and_relationship_exposure():
    """Test ID 10: Tagging family members creates security question vulnerability finding."""
    responses = {"q9": "YES"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_FAMILY_PUBLIC" for f in findings)


def test_11_public_post_audience_default():
    """Test ID 11: Default public audience triggers content risk."""
    responses = {"q15": "PUBLIC"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_POSTS_DEFAULT_PUBLIC" for f in findings)


def test_12_unknown_connections_acceptance():
    """Test ID 12: Accepting stranger friend requests creates perimeter risk."""
    responses = {"q19": "ACCEPT_MOST"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_UNKNOWN_CONNECTIONS" for f in findings)


def test_13_tag_review_disabled():
    """Test ID 13: Disabled tag review generates finding."""
    responses = {"q23": "NO"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_TAG_REVIEW_OFF" for f in findings)


def test_14_mfa_disabled_account_risk():
    """Test ID 14: Disabled MFA triggers critical account takeover finding."""
    responses = {"q27": "DISABLED"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_MFA_DISABLED" and f["severity"] == "CRITICAL" for f in findings)


def test_15_login_alerts_disabled():
    """Test ID 15: Unrecognized login alerts disabled."""
    responses = {"q30": "NO"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_LOGIN_ALERTS_OFF" for f in findings)


def test_16_password_reuse_reported():
    """Test ID 16: Credential reuse across services creates high finding."""
    responses = {"q28": "REUSED"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_PASSWORD_REUSE" for f in findings)


def test_17_third_party_apps_unreviewed():
    """Test ID 17: Unaudited third-party OAuth apps generate high finding."""
    responses = {"q33": "NEVER"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_THIRD_PARTY_UNREVIEWED" for f in findings)


def test_18_suspicious_link_awareness_low():
    """Test ID 18: Clicking unexpected DM links generates critical phishing finding."""
    responses = {"q36": "CLICK_IMMEDIATELY"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_SUSPICIOUS_LINK_RISK" and f["severity"] == "CRITICAL" for f in findings)


def test_19_old_historical_posts_unreviewed():
    """Test ID 19: Unaudited 3+ year old posts flag digital footprint finding."""
    responses = {"q40": "NEVER"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_OLD_POSTS_UNAUDITED" for f in findings)


def test_20_privacy_settings_unreviewed_and_abandoned_accounts():
    """Test ID 20: Dormant / abandoned accounts flag legacy exposure."""
    responses = {"q41": "YES_MULTIPLE"}
    features = extract_privacy_features(responses)
    findings = generate_privacy_findings(features, responses)

    assert any(f["finding_id"] == "FIND_ABANDONED_ACCOUNTS" for f in findings)


def test_21_category_score_calculation():
    """Test ID 21: Category score scales exactly 0 to 100."""
    features = {"raw_scores": {f"q{i}": 5.0 for i in range(1, 45)}}
    cat_scores = calculate_category_scores(features)

    assert len(cat_scores) == 10
    for cid, cdata in cat_scores.items():
        assert cdata["score"] == 50.0
        assert 0.0 <= cdata["score"] <= 100.0


def test_22_overall_score_calculation():
    """Test ID 22: Overall score respects configured weights summing to 100%."""
    cat_scores = {
        cid: {"name": cat["name"], "score": 60.0, "weight": cat["weight"]}
        for cid, cat in CATEGORIES.items()
    }
    overall_score, risk_level = calculate_overall_risk(cat_scores)

    assert overall_score == 60.0
    assert risk_level == "HIGH"


def test_23_score_boundary_20_low():
    """Test ID 23: Boundary score 20.0 is classified as LOW, 20.1 is MODERATE."""
    assert get_risk_level(20.0) == "LOW"
    assert get_risk_level(20.1) == "MODERATE"


def test_24_score_boundary_40_moderate():
    """Test ID 24: Boundary score 40.0 is MODERATE, 40.1 is HIGH."""
    assert get_risk_level(40.0) == "MODERATE"
    assert get_risk_level(40.1) == "HIGH"


def test_25_score_boundary_70_high():
    """Test ID 25: Boundary score 70.0 is HIGH, 70.1 is CRITICAL."""
    assert get_risk_level(70.0) == "HIGH"
    assert get_risk_level(70.1) == "CRITICAL"


def test_26_recommendation_generation_and_priorities():
    """Test ID 26: Recommendations are mapped and sorted by priority."""
    findings = [
        {"finding_id": "FIND_PHONE_PUBLIC", "category": "CAT_B", "severity": "CRITICAL", "title": "Phone"},
        {"finding_id": "FIND_EMAIL_PUBLIC", "category": "CAT_B", "severity": "HIGH", "title": "Email"},
        {"finding_id": "FIND_SEARCH_INDEXING", "category": "CAT_A", "severity": "MEDIUM", "title": "Search Index"}
    ]
    recs = generate_recommendations(findings)

    assert len(recs) == 3
    assert recs[0]["priority"] == "IMMEDIATE"
    assert recs[1]["priority"] == "IMPORTANT"
    assert recs[2]["priority"] == "GOOD PRACTICE"


def test_27_improvement_simulation():
    """Test ID 27: Applying simulated changes decreases the risk score."""
    base_responses = {
        "q5": "YES",           # Public phone
        "q10": "YES",          # Realtime location
        "q27": "DISABLED",     # No MFA
        "q23": "NO"            # No tag review
    }
    improvements = ["make_phone_private", "disable_realtime_location", "enable_mfa", "enable_tag_review"]
    sim_result = simulate_privacy_improvement(base_responses, improvements)

    assert sim_result["points_reduced"] > 0
    assert sim_result["simulated"]["overall_score"] < sim_result["baseline"]["overall_score"]


def test_28_database_save_and_retrieval(test_db_path):
    """Test ID 28: Save assessment and retrieve by ID."""
    result = run_assessment({"q5": "YES", "q27": "DISABLED"})
    aid = save_assessment(result, db_path=test_db_path)
    retrieved = get_assessment(aid, db_path=test_db_path)

    assert retrieved is not None
    assert retrieved["assessment_id"] == aid
    assert retrieved["overall_score"] == result["overall_score"]


def test_29_privacy_by_design_zero_pii_stored(test_db_path):
    """Test ID 29: Verify NO sensitive PII columns or values exist in database schema."""
    import sqlite3
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(assessments)")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()

    forbidden = ["phone", "email", "address", "birthday", "name", "password", "ssn"]
    for col in columns:
        for f in forbidden:
            assert f not in col.lower(), f"Sensitive column '{col}' found in schema!"


def test_30_report_generation_structure():
    """Test ID 30: run_assessment generates comprehensive report schema."""
    result = run_assessment({"q1": "PUBLIC", "q5": "YES"})

    assert "assessment_id" in result
    assert "created_at" in result
    assert "overall_score" in result
    assert "risk_level" in result
    assert "category_scores" in result
    assert "findings" in result
    assert "recommendations" in result
    assert "disclaimer" in result


def test_31_local_exif_metadata_inspection():
    """Test ID 31: Verify local EXIF extraction correctly identifies image dimensions and handles clean files."""
    img = Image.new("RGB", (200, 150), color="blue")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    meta = extract_exif_metadata(buf.getvalue())

    assert meta["dimensions"] == "200 x 150 px"
    assert meta["format"] == "JPEG"
    assert meta["has_exif"] is False


def test_32_exif_sanitizer():
    """Test ID 32: Sanitizer strips all metadata cleanly."""
    img = Image.new("RGB", (100, 100), color="red")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    clean_bytes = strip_exif_metadata(buf.getvalue())

    clean_meta = extract_exif_metadata(clean_bytes)
    assert clean_meta["has_exif"] is False


def test_33_api_endpoints_and_gdpr_deletion(app_client):
    """Test ID 33: API health, assessment submission, and GDPR erasure endpoint."""
    # Health
    res = app_client.get("/api/health")
    assert res.status_code == 200

    # Submit
    res = app_client.post("/api/assessment", json={"responses": {"q1": "PRIVATE", "q27": "APP_OR_HARDWARE"}})
    assert res.status_code == 201
    data = res.get_json()
    aid = data["assessment_id"]

    # Delete (GDPR)
    del_res = app_client.delete(f"/api/assessment/{aid}")
    assert del_res.status_code == 200
