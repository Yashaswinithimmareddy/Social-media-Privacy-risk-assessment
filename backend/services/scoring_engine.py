"""
Social Media Privacy Risk Assessment Framework
Scoring Engine & Feature Extraction

Transforms self-reported questionnaire answers into normalized numeric risk features,
computes category-level privacy scores (0-100), and calculates the weighted overall
privacy risk score and classification.
"""

from typing import Dict, Any, Tuple
from backend.services.questionnaire_data import QUESTIONS, QUESTION_MAP, CATEGORIES, CATEGORY_WEIGHTS

def extract_privacy_features(responses: Dict[str, str]) -> Dict[str, Any]:
    """
    Converts raw response keys into normalized numerical risk features (0 to 10).
    Also derives behavioral interaction metrics.
    
    Args:
        responses: Dictionary mapping question IDs (q1..q44) to chosen option values.
        
    Returns:
        Structured dictionary of feature scores and derived flags.
    """
    feature_scores: Dict[str, float] = {}
    exposure_flags: Dict[str, bool] = {}

    for q in QUESTIONS:
        qid = q["id"]
        val = responses.get(qid)
        score = 0.0
        
        # Match option value to preconfigured risk score
        matched = False
        if val is not None:
            for opt in q["options"]:
                if opt["value"] == val:
                    score = float(opt["risk_score"])
                    matched = True
                    break
        if not matched:
            # Default to moderate risk if question omitted or not recognized
            score = 5.0
            
        feature_scores[qid] = score
        # Flag as high-risk if score is 7 or above
        exposure_flags[f"{qid}_high_risk"] = (score >= 7.0)

    # Derived composite risk indicators
    features = {
        "raw_scores": feature_scores,
        "flags": exposure_flags,
        # Direct summary flags for quick rule checks
        "public_phone_exposed": responses.get("q5") == "YES",
        "public_email_exposed": responses.get("q6") == "YES",
        "full_birthday_exposed": responses.get("q7") == "FULL_BIRTHDAY",
        "realtime_location_enabled": responses.get("q10") in ["YES", "SOMETIMES"],
        "mfa_disabled": responses.get("q27") == "DISABLED",
        "password_reused": responses.get("q28") in ["REUSED", "SLIGHT_VARIATION"],
        "unknown_connections_accepted": responses.get("q19") in ["ACCEPT_MOST", "SOMETIMES"],
        "tag_review_disabled": responses.get("q23") in ["NO", "NOT_SURE"],
        "third_party_apps_unreviewed": responses.get("q33") in ["NEVER", "RARELY"],
        "old_posts_unreviewed": responses.get("q40") in ["NEVER", "RARELY"]
    }
    return features


def calculate_category_scores(features: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Calculates category-wise privacy scores scaled from 0 (Safe) to 100 (Critical Exposure).
    
    Returns:
        Dictionary mapping category IDs to score, weight, name, and risk level.
    """
    raw_scores = features.get("raw_scores", {})
    category_results: Dict[str, Dict[str, Any]] = {}

    for cat_id, cat_info in CATEGORIES.items():
        # Get all questions belonging to this category
        cat_questions = [q for q in QUESTIONS if q["category"] == cat_id]
        if not cat_questions:
            continue
            
        total_points = sum(raw_scores.get(q["id"], 5.0) for q in cat_questions)
        max_possible = len(cat_questions) * 10.0
        
        # Scale to 0 - 100
        category_score = round((total_points / max_possible) * 100.0, 1)
        category_score = max(0.0, min(100.0, category_score))
        
        category_results[cat_id] = {
            "category_id": cat_id,
            "name": cat_info["name"],
            "score": category_score,
            "weight": cat_info["weight"],
            "risk_level": get_risk_level(category_score),
            "description": cat_info["description"]
        }

    return category_results


def calculate_overall_risk(
    category_scores: Dict[str, Dict[str, Any]], 
    custom_weights: Dict[str, float] = None
) -> Tuple[float, str]:
    """
    Calculates the final weighted Privacy Risk Score (0-100) and assigns risk classification.
    
    Weights configuration:
    - Profile Visibility: 10%
    - Personal Information: 15%
    - Location Privacy: 15%
    - Posts & Content: 10%
    - Friends & Followers: 10%
    - Tagging & Mentions: 5%
    - Authentication & Account Security: 15%
    - Third-Party Apps: 5%
    - Social Engineering: 10%
    - Digital Footprint: 5%
    Total: 100%
    """
    weights = custom_weights if custom_weights else CATEGORY_WEIGHTS
    
    # Normalize weights so they always sum up to 1.0 even if adjusted
    weight_sum = sum(weights.get(cid, 0.1) for cid in CATEGORIES.keys())
    if weight_sum <= 0:
        weight_sum = 1.0

    weighted_total = 0.0
    for cat_id in CATEGORIES.keys():
        cat_data = category_scores.get(cat_id, {})
        cat_score = cat_data.get("score", 50.0)
        norm_weight = weights.get(cat_id, 0.10) / weight_sum
        weighted_total += cat_score * norm_weight

    overall_score = round(weighted_total, 1)
    overall_score = max(0.0, min(100.0, overall_score))
    risk_level = get_risk_level(overall_score)
    
    return overall_score, risk_level


def get_risk_level(score: float) -> str:
    """
    Assigns qualitative risk tier based on numerical score:
    0–20:   LOW
    21–40:  MODERATE
    41–70:  HIGH
    71–100: CRITICAL
    """
    if score <= 20.0:
        return "LOW"
    elif score <= 40.0:
        return "MODERATE"
    elif score <= 70.0:
        return "HIGH"
    else:
        return "CRITICAL"
