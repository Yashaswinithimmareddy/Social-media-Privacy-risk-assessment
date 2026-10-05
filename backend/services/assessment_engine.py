"""
Social Media Privacy Risk Assessment Framework
Master Assessment Engine

Coordinates the entire assessment pipeline: input validation, feature extraction,
category scoring, overall risk scoring, findings detection, and recommendation generation.
Strictly adheres to Privacy by Design: zero PII processing or retention.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List

from backend.services.questionnaire_data import QUESTIONS, QUESTION_MAP, CATEGORIES
from backend.services.scoring_engine import (
    extract_privacy_features,
    calculate_category_scores,
    calculate_overall_risk,
    get_risk_level
)
from backend.services.findings_engine import generate_privacy_findings
from backend.services.recommendation_engine import generate_recommendations

def validate_responses(responses: Dict[str, str]) -> Dict[str, str]:
    """
    Validates user questionnaire submissions.
    Ensures that values submitted correspond to allowed options for each question.
    Sanitizes keys and removes any unwhitelisted fields (ensuring zero PII ingestion).
    """
    cleaned_responses: Dict[str, str] = {}
    
    for q in QUESTIONS:
        qid = q["id"]
        val = responses.get(qid)
        if val is not None:
            # Check if val is in allowed options
            valid_vals = {opt["value"] for opt in q["options"]}
            if str(val) in valid_vals:
                cleaned_responses[qid] = str(val)
            else:
                # Default to safe moderate option if invalid
                cleaned_responses[qid] = q["options"][0]["value"]
        else:
            # If omitted, select middle or default option
            cleaned_responses[qid] = q["options"][0]["value"]

    return cleaned_responses


def run_assessment(responses: Dict[str, str], custom_weights: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Executes a complete privacy risk assessment for a given set of responses.
    
    Returns:
        Structured assessment result dictionary containing:
        - assessment_id
        - timestamp
        - overall_score
        - risk_level
        - category_scores
        - findings (sorted by severity)
        - recommendations (sorted by priority)
        - summary statistics
    """
    assessment_id = f"PRA-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.now(timezone.utc).isoformat()

    # 1. Input validation & PII stripping
    cleaned_responses = validate_responses(responses)

    # 2. Feature extraction
    features = extract_privacy_features(cleaned_responses)

    # 3. Category risk scoring (0-100)
    category_scores = calculate_category_scores(features)

    # 4. Overall risk calculation (0-100)
    overall_score, risk_level = calculate_overall_risk(category_scores, custom_weights)

    # 5. Generate specific findings
    findings = generate_privacy_findings(features, cleaned_responses)

    # 6. Generate prioritized recommendations
    recommendations = generate_recommendations(findings)

    # 7. Identify top vulnerable categories
    sorted_categories = sorted(
        category_scores.values(), 
        key=lambda x: x["score"], 
        reverse=True
    )
    high_risk_categories = [c["name"] for c in sorted_categories if c["score"] >= 41.0]

    # 8. Security controls count
    total_controls = len(findings)
    immediate_actions = [r for r in recommendations if r["priority"] == "IMMEDIATE"]
    important_actions = [r for r in recommendations if r["priority"] == "IMPORTANT"]
    good_practice_actions = [r for r in recommendations if r["priority"] == "GOOD PRACTICE"]

    return {
        "assessment_id": assessment_id,
        "created_at": timestamp,
        "overall_score": overall_score,
        "risk_level": risk_level,
        "category_scores": category_scores,
        "findings": findings,
        "findings_count": len(findings),
        "recommendations": recommendations,
        "high_risk_categories": high_risk_categories,
        "stats": {
            "total_questions_answered": len(cleaned_responses),
            "critical_findings": sum(1 for f in findings if f["severity"] == "CRITICAL"),
            "high_findings": sum(1 for f in findings if f["severity"] == "HIGH"),
            "medium_findings": sum(1 for f in findings if f["severity"] == "MEDIUM"),
            "low_findings": sum(1 for f in findings if f["severity"] == "LOW"),
            "immediate_actions": len(immediate_actions),
            "important_actions": len(important_actions),
            "good_practice_actions": len(good_practice_actions)
        },
        "cleaned_responses": cleaned_responses,
        "disclaimer": (
            "Educational Risk Framework Disclaimer: This privacy risk assessment is designed "
            "exclusively for defensive education and cybersecurity awareness. Scores reflect "
            "self-reported exposure configurations and do not guarantee whether an account is "
            "or will be compromised."
        )
    }
