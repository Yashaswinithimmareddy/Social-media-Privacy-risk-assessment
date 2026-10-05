"""
Social Media Privacy Risk Assessment Framework
Privacy Improvement Simulator

Simulates the impact of hypothetical security & privacy hardening actions on the
user's overall risk score and category levels. Provides users with quantifiable
feedback on how simple privacy changes decrease their attack surface.
"""

from typing import Dict, Any, List
from backend.services.scoring_engine import (
    extract_privacy_features,
    calculate_category_scores,
    calculate_overall_risk,
    get_risk_level
)

# Standard simulator toggles mapped to question IDs and hardened values
SIMULATION_PRESETS = {
    "make_phone_private": {
        "label": "Make mobile phone number private / hidden",
        "question_id": "q5",
        "hardened_value": "NO",
        "category": "CAT_B",
        "category_name": "Personal Information"
    },
    "hide_birth_year": {
        "label": "Hide birth year or full birth date",
        "question_id": "q7",
        "hardened_value": "HIDDEN",
        "category": "CAT_B",
        "category_name": "Personal Information"
    },
    "disable_realtime_location": {
        "label": "Disable real-time live location broadcasts",
        "question_id": "q10",
        "hardened_value": "NO",
        "category": "CAT_C",
        "category_name": "Location Privacy"
    },
    "delay_venue_checkins": {
        "label": "Delay venue check-ins until after leaving",
        "question_id": "q11",
        "hardened_value": "AFTER_LEAVING",
        "category": "CAT_C",
        "category_name": "Location Privacy"
    },
    "enable_mfa": {
        "label": "Enable Multi-Factor Authentication (MFA / 2FA)",
        "question_id": "q27",
        "hardened_value": "APP_OR_HARDWARE",
        "category": "CAT_G",
        "category_name": "Authentication & Account Security"
    },
    "unique_password": {
        "label": "Use a completely unique password & password manager",
        "question_id": "q28",
        "hardened_value": "COMPLETELY_UNIQUE",
        "category": "CAT_G",
        "category_name": "Authentication & Account Security"
    },
    "enable_login_alerts": {
        "label": "Turn on unrecognized login alerts",
        "question_id": "q30",
        "hardened_value": "YES",
        "category": "CAT_G",
        "category_name": "Authentication & Account Security"
    },
    "enable_tag_review": {
        "label": "Enable tag review before posts appear on profile",
        "question_id": "q23",
        "hardened_value": "YES",
        "category": "CAT_F",
        "category_name": "Tagging & Mentions"
    },
    "restrict_unknown_connections": {
        "label": "Reject or thoroughly verify unknown friend/follow requests",
        "question_id": "q19",
        "hardened_value": "REJECT_UNKNOWN",
        "category": "CAT_E",
        "category_name": "Friends & Followers"
    },
    "audit_third_party_apps": {
        "label": "Audit and revoke unused third-party application permissions",
        "question_id": "q33",
        "hardened_value": "REGULARLY",
        "category": "CAT_H",
        "category_name": "Third-Party Apps"
    },
    "limit_past_posts": {
        "label": "Review and mass-privatize historical public posts",
        "question_id": "q40",
        "hardened_value": "REGULARLY",
        "category": "CAT_J",
        "category_name": "Digital Footprint"
    },
    "verify_phishing_links": {
        "label": "Adopt strict out-of-band verification for suspicious DMs",
        "question_id": "q36",
        "hardened_value": "VERIFY_OUT_OF_BAND",
        "category": "CAT_I",
        "category_name": "Messaging & Social Engineering"
    }
}


def simulate_privacy_improvement(
    original_responses: Dict[str, str],
    selected_improvements: List[str]
) -> Dict[str, Any]:
    """
    Takes the original assessment responses, applies a list of simulated improvements,
    and recalculates the resulting risk score and reduction metrics.
    
    Args:
        original_responses: Dict mapping q1..q44 to answer values.
        selected_improvements: List of preset keys from SIMULATION_PRESETS.
        
    Returns:
        Structured simulation comparison dictionary.
    """
    # 1. Calculate baseline current score
    current_features = extract_privacy_features(original_responses)
    current_cat_scores = calculate_category_scores(current_features)
    current_score, current_risk_level = calculate_overall_risk(current_cat_scores)

    # 2. Clone responses and apply simulated changes
    simulated_responses = dict(original_responses)
    applied_changes_details = []

    for improvement_key in selected_improvements:
        preset = SIMULATION_PRESETS.get(improvement_key)
        if preset:
            qid = preset["question_id"]
            old_val = simulated_responses.get(qid)
            new_val = preset["hardened_value"]
            simulated_responses[qid] = new_val
            applied_changes_details.append({
                "key": improvement_key,
                "label": preset["label"],
                "category": preset["category"],
                "category_name": preset["category_name"],
                "previous_value": old_val,
                "simulated_value": new_val
            })

    # 3. Calculate simulated score
    sim_features = extract_privacy_features(simulated_responses)
    sim_cat_scores = calculate_category_scores(sim_features)
    sim_score, sim_risk_level = calculate_overall_risk(sim_cat_scores)

    points_reduced = round(max(0.0, current_score - sim_score), 1)
    percentage_improvement = round((points_reduced / current_score * 100.0), 1) if current_score > 0 else 0.0

    return {
        "baseline": {
            "overall_score": current_score,
            "risk_level": current_risk_level,
            "category_scores": current_cat_scores
        },
        "simulated": {
            "overall_score": sim_score,
            "risk_level": sim_risk_level,
            "category_scores": sim_cat_scores
        },
        "points_reduced": points_reduced,
        "percentage_improvement": percentage_improvement,
        "applied_changes": applied_changes_details,
        "available_presets": SIMULATION_PRESETS,
        "disclaimer": (
            "Educational Risk Simulation: This reduction is an algorithmic estimation based on "
            "standard risk reduction weights. It serves as educational guidance and does not guarantee "
            "immunity from cyber threats or account compromise."
        )
    }
