"""
Social Media Privacy Risk Assessment Framework
Synthetic Profile Dataset Generator

Generates 1,000+ purely synthetic, fictional privacy assessment records
conforming to the defensive cybersecurity risk scoring engine.
Zero personal data scraping; completely simulated research data.
Saves CSV to data/social_media_privacy_assessments.csv and seeds the SQLite database.
"""

import os
import random
import csv
from datetime import datetime, timedelta, timezone

# Ensure project root is in path
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.services.scoring_engine import (
    extract_privacy_features,
    calculate_category_scores,
    calculate_overall_risk
)
from backend.services.assessment_engine import run_assessment
from backend.models.database import save_assessment, init_db

OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "social_media_privacy_assessments.csv")

def generate_synthetic_records(num_records: int = 1200) -> None:
    """
    Generates synthetic survey responses across diverse behavioral privacy personas:
    1. 'Privacy Conscious' (~25%) - Private settings, MFA active, delayed posting
    2. 'Average User' (~45%) - Mixed settings, SMS MFA, occasional check-ins
    3. 'High Exposure / Influencer Persona' (~30%) - Public profile, live check-ins, reused passwords
    """
    print(f"[*] Generating {num_records} synthetic privacy assessment records...")
    random.seed(42)  # For reproducible scientific benchmark data

    records = []
    base_date = datetime.now(timezone.utc) - timedelta(days=90)

    # Option pools per question
    vis_options = ["PUBLIC", "FRIENDS_OF_FRIENDS", "FRIENDS_ONLY", "PRIVATE"]
    search_options = ["YES", "NOT_SURE", "NO"]
    bool_options = ["YES", "NO", "NOT_SURE"]
    birthday_options = ["FULL_BIRTHDAY", "DAY_MONTH_ONLY", "HIDDEN"]
    location_options = ["YES", "SOMETIMES", "NO"]
    checkin_options = ["IMMEDIATELY", "SOMETIMES_LATER", "AFTER_LEAVING", "NEVER_CHECKIN"]
    mfa_options = ["DISABLED", "SMS_ONLY", "APP_OR_HARDWARE"]
    pwd_options = ["REUSED", "SLIGHT_VARIATION", "COMPLETELY_UNIQUE"]
    connections_options = ["ACCEPT_MOST", "SOMETIMES", "VERIFY_FIRST", "REJECT_UNKNOWN"]
    audit_options = ["NEVER", "RARELY", "REGULARLY"]

    for i in range(1, num_records + 1):
        profile_id = f"SYNTH_USER_{i:04d}"
        persona = random.choices(["CONSCIOUS", "AVERAGE", "HIGH_EXPOSURE"], weights=[0.25, 0.45, 0.30])[0]

        if persona == "CONSCIOUS":
            q_responses = {
                "q1": random.choice(["FRIENDS_ONLY", "PRIVATE"]),
                "q2": "NO",
                "q3": random.choice(["FRIENDS", "ONLY_ME"]),
                "q4": "RESTRICTED",
                "q5": "NO",
                "q6": "NO",
                "q7": random.choice(["DAY_MONTH_ONLY", "HIDDEN"]),
                "q8": "NO",
                "q9": "NO",
                "q10": "NO",
                "q11": random.choice(["AFTER_LEAVING", "NEVER_CHECKIN"]),
                "q12": "NO",
                "q13": "NO",
                "q14": "NO",
                "q15": random.choice(["FRIENDS", "CUSTOM_LISTS"]),
                "q16": "NEVER",
                "q17": "NO",
                "q18": "NEVER",
                "q19": random.choice(["VERIFY_FIRST", "REJECT_UNKNOWN"]),
                "q20": "REGULARLY",
                "q21": "ALWAYS",
                "q22": random.choice(["FILTERED_REQUESTS", "FRIENDS_ONLY"]),
                "q23": "YES",
                "q24": random.choice(["FRIENDS_ONLY", "NO_ONE"]),
                "q25": "DISABLED",
                "q26": random.choice(["PEOPLE_I_FOLLOW", "NO_ONE"]),
                "q27": "APP_OR_HARDWARE",
                "q28": "COMPLETELY_UNIQUE",
                "q29": "PASSWORD_MANAGER",
                "q30": "YES",
                "q31": "REGULARLY",
                "q32": "RARELY_OR_NEVER",
                "q33": "REGULARLY",
                "q34": "NO_LEAST_PRIVILEGE",
                "q35": "NEVER",
                "q36": "VERIFY_OUT_OF_BAND",
                "q37": "NEVER",
                "q38": "CALL_OUT_OF_BAND",
                "q39": "IGNORE_AND_BLOCK",
                "q40": "REGULARLY",
                "q41": "SECURED_OR_DELETED",
                "q42": "SEGREGATED",
                "q43": "REGULARLY",
                "q44": "DOWNLOADED_AND_REVIEWED"
            }
        elif persona == "HIGH_EXPOSURE":
            q_responses = {
                "q1": "PUBLIC",
                "q2": "YES",
                "q3": "PUBLIC",
                "q4": "PUBLIC",
                "q5": random.choice(["YES", "NOT_SURE"]),
                "q6": "YES",
                "q7": "FULL_BIRTHDAY",
                "q8": random.choice(["YES", "CITY_ONLY"]),
                "q9": "YES",
                "q10": "YES",
                "q11": "IMMEDIATELY",
                "q12": "YES",
                "q13": "YES",
                "q14": "YES",
                "q15": "PUBLIC",
                "q16": random.choice(["YES", "SOMETIMES"]),
                "q17": "YES",
                "q18": "YES",
                "q19": "ACCEPT_MOST",
                "q20": "NEVER",
                "q21": "NEVER",
                "q22": "ANYONE",
                "q23": "NO",
                "q24": "EVERYONE",
                "q25": "ENABLED",
                "q26": "EVERYONE",
                "q27": "DISABLED",
                "q28": "REUSED",
                "q29": "NO",
                "q30": "NO",
                "q31": "NEVER",
                "q32": "FREQUENTLY",
                "q33": "NEVER",
                "q34": "YES",
                "q35": "YES",
                "q36": "CLICK_IMMEDIATELY",
                "q37": random.choice(["YES_HELP", "HESITATE"]),
                "q38": "TRUST_URGENCY",
                "q39": "ENGAGE_OFTEN",
                "q40": "NEVER",
                "q41": "YES_MULTIPLE",
                "q42": "SAME_EVERYWHERE",
                "q43": "NEVER",
                "q44": "NEVER"
            }
        else:  # AVERAGE
            q_responses = {
                "q1": random.choice(["PUBLIC", "FRIENDS_OF_FRIENDS", "FRIENDS_ONLY"]),
                "q2": random.choice(["NOT_SURE", "YES", "NO"]),
                "q3": random.choice(["PUBLIC", "FRIENDS"]),
                "q4": random.choice(["PUBLIC", "FRIENDS"]),
                "q5": random.choice(["NO", "NOT_SURE", "YES"]),
                "q6": random.choice(["NO", "YES"]),
                "q7": random.choice(["DAY_MONTH_ONLY", "FULL_BIRTHDAY"]),
                "q8": random.choice(["CITY_ONLY", "NO"]),
                "q9": random.choice(["SOMETIMES", "NO"]),
                "q10": random.choice(["SOMETIMES", "NO"]),
                "q11": random.choice(["SOMETIMES_LATER", "IMMEDIATELY"]),
                "q12": random.choice(["SOMETIMES", "NO"]),
                "q13": random.choice(["SOMETIMES", "NO"]),
                "q14": random.choice(["NOT_SURE", "YES"]),
                "q15": random.choice(["PUBLIC", "FRIENDS"]),
                "q16": random.choice(["SOMETIMES", "NEVER"]),
                "q17": random.choice(["SOMETIMES", "NO"]),
                "q18": random.choice(["SOMETIMES", "NEVER"]),
                "q19": random.choice(["SOMETIMES", "VERIFY_FIRST"]),
                "q20": random.choice(["RARELY", "NEVER"]),
                "q21": random.choice(["SOMETIMES", "NEVER"]),
                "q22": random.choice(["FILTERED_REQUESTS", "ANYONE"]),
                "q23": random.choice(["NO", "NOT_SURE", "YES"]),
                "q24": random.choice(["FRIENDS_ONLY", "EVERYONE"]),
                "q25": random.choice(["NOT_SURE", "ENABLED"]),
                "q26": random.choice(["EVERYONE", "PEOPLE_I_FOLLOW"]),
                "q27": random.choice(["SMS_ONLY", "DISABLED", "APP_OR_HARDWARE"]),
                "q28": random.choice(["SLIGHT_VARIATION", "REUSED", "COMPLETELY_UNIQUE"]),
                "q29": random.choice(["BROWSER", "NO"]),
                "q30": random.choice(["NOT_SURE", "YES"]),
                "q31": random.choice(["RARELY", "NEVER"]),
                "q32": random.choice(["OCCASIONALLY", "FREQUENTLY"]),
                "q33": random.choice(["RARELY", "NEVER"]),
                "q34": random.choice(["NOT_SURE", "YES"]),
                "q35": random.choice(["SOMETIMES", "NEVER"]),
                "q36": random.choice(["INSPECT_URL", "VERIFY_OUT_OF_BAND"]),
                "q37": random.choice(["HESITATE", "NEVER"]),
                "q38": random.choice(["REPLY_IN_DM", "CALL_OUT_OF_BAND"]),
                "q39": random.choice(["SOMETIMES", "IGNORE_AND_BLOCK"]),
                "q40": random.choice(["RARELY", "NEVER"]),
                "q41": random.choice(["MAYBE_ONE", "YES_MULTIPLE"]),
                "q42": random.choice(["SOME_OVERLAP", "SAME_EVERYWHERE"]),
                "q43": random.choice(["YEARLY", "NEVER"]),
                "q44": random.choice(["AWARE_BUT_NOT_DONE", "NEVER"])
            }

        # Calculate scores using the actual framework scoring engine
        features = extract_privacy_features(q_responses)
        cat_scores = calculate_category_scores(features)
        overall_score, risk_level = calculate_overall_risk(cat_scores)

        # Simulation effect
        sim_score = max(5.0, round(overall_score * random.uniform(0.35, 0.65), 1))
        pts_reduced = round(overall_score - sim_score, 1)

        simulated_date = base_date + timedelta(
            days=random.randint(0, 90),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        record = {
            "profile_id": profile_id,
            "persona": persona,
            "created_at": simulated_date.strftime("%Y-%m-%d %H:%M:%S"),
            "profile_visibility": q_responses["q1"],
            "search_engine_indexing": q_responses["q2"],
            "phone_public": q_responses["q5"],
            "email_public": q_responses["q6"],
            "birthday_public": q_responses["q7"],
            "location_public": q_responses["q8"],
            "relationship_public": q_responses["q9"],
            "realtime_location_sharing": q_responses["q10"],
            "venue_checkins": q_responses["q11"],
            "travel_posts": q_responses["q12"],
            "posts_audience": q_responses["q15"],
            "sensitive_docs_photographed": q_responses["q16"],
            "unknown_connections": q_responses["q19"],
            "tag_review_enabled": q_responses["q23"],
            "mfa_status": q_responses["q27"],
            "password_reuse_reported": q_responses["q28"],
            "login_alerts_enabled": q_responses["q30"],
            "third_party_apps_reviewed": q_responses["q33"],
            "suspicious_link_awareness": q_responses["q36"],
            "otp_sharing_behavior": q_responses["q37"],
            "old_posts_reviewed": q_responses["q40"],
            "score_profile_visibility": cat_scores["CAT_A"]["score"],
            "score_personal_info": cat_scores["CAT_B"]["score"],
            "score_location": cat_scores["CAT_C"]["score"],
            "score_posts_content": cat_scores["CAT_D"]["score"],
            "score_friends_followers": cat_scores["CAT_E"]["score"],
            "score_tagging": cat_scores["CAT_F"]["score"],
            "score_account_security": cat_scores["CAT_G"]["score"],
            "score_third_party_apps": cat_scores["CAT_H"]["score"],
            "score_social_engineering": cat_scores["CAT_I"]["score"],
            "score_digital_footprint": cat_scores["CAT_J"]["score"],
            "overall_privacy_risk_score": overall_score,
            "risk_level": risk_level,
            "simulated_score": sim_score,
            "points_reduced": pts_reduced
        }
        records.append(record)

    # Write to CSV
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    fieldnames = list(records[0].keys())

    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"[+] Successfully wrote {len(records)} records to {OUTPUT_CSV}")

    # Seed the SQLite database with 150 diverse records so the dashboard has instant live analytics
    print("[*] Seeding database with diverse sample records for dashboard visualization...")
    init_db()
    for rec in records[:150]:
        # Formulate assessment result dictionary
        result_dict = {
            "assessment_id": rec["profile_id"].replace("SYNTH_USER_", "SYNTH-"),
            "created_at": rec["created_at"],
            "overall_score": rec["overall_privacy_risk_score"],
            "risk_level": rec["risk_level"],
            "category_scores": {
                "CAT_A": {"name": "Profile Visibility", "score": rec["score_profile_visibility"], "weight": 0.10},
                "CAT_B": {"name": "Personal Information", "score": rec["score_personal_info"], "weight": 0.15},
                "CAT_C": {"name": "Location Privacy", "score": rec["score_location"], "weight": 0.15},
                "CAT_D": {"name": "Posts & Content", "score": rec["score_posts_content"], "weight": 0.10},
                "CAT_E": {"name": "Friends & Followers", "score": rec["score_friends_followers"], "weight": 0.10},
                "CAT_F": {"name": "Tagging & Mentions", "score": rec["score_tagging"], "weight": 0.05},
                "CAT_G": {"name": "Authentication & Account Security", "score": rec["score_account_security"], "weight": 0.15},
                "CAT_H": {"name": "Third-Party Apps", "score": rec["score_third_party_apps"], "weight": 0.05},
                "CAT_I": {"name": "Messaging & Social Engineering", "score": rec["score_social_engineering"], "weight": 0.10},
                "CAT_J": {"name": "Digital Footprint", "score": rec["score_digital_footprint"], "weight": 0.05},
            },
            "findings": [
                {
                    "finding_id": "FIND_PHONE_PUBLIC",
                    "category": "CAT_B",
                    "severity": "CRITICAL",
                    "title": "Mobile Phone Number Publicly Visible",
                    "description": "Phone number publicly viewable.",
                    "technical_impact": "Direct vector for SIM swapping and smishing."
                } if rec["phone_public"] == "YES" else None,
                {
                    "finding_id": "FIND_MFA_DISABLED",
                    "category": "CAT_G",
                    "severity": "CRITICAL",
                    "title": "Multi-Factor Authentication (MFA) Disabled",
                    "description": "Password only.",
                    "technical_impact": "Vulnerable to credential stuffing."
                } if rec["mfa_status"] == "DISABLED" else None,
                {
                    "finding_id": "FIND_REALTIME_LOCATION",
                    "category": "CAT_C",
                    "severity": "CRITICAL",
                    "title": "Real-Time Location Broadcasts Enabled",
                    "description": "Live location stamps.",
                    "technical_impact": "Enables physical surveillance."
                } if rec["realtime_location_sharing"] in ["YES", "SOMETIMES"] else None,
            ],
            "recommendations": []
        }
        # Filter None findings
        result_dict["findings"] = [f for f in result_dict["findings"] if f is not None]
        try:
            save_assessment(result_dict)
        except Exception:
            pass

    print("[+] Database successfully seeded!")

if __name__ == "__main__":
    generate_synthetic_records(1200)
