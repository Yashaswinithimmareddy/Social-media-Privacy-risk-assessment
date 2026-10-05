"""
Social Media Privacy Risk Assessment Framework
Findings Engine

Analyzes privacy feature extractions and detected exposure vectors to generate
specific, contextual privacy and security findings ranked by severity.
"""

from typing import Dict, List, Any
from backend.services.questionnaire_data import QUESTION_MAP

FINDING_DEFINITIONS = {
    # Personal Information
    "FIND_PHONE_PUBLIC": {
        "condition": lambda r, f: r.get("q5") == "YES",
        "category": "CAT_B",
        "severity": "CRITICAL",
        "title": "Mobile Phone Number Publicly Visible",
        "description": "Your phone number is reported as publicly viewable on your profile or bio.",
        "technical_impact": "Direct vector for SIM-swapping, SMS phishing (smishing), unauthorized WhatsApp re-registration, and reverse lookups in leaked breaches."
    },
    "FIND_BIRTHDAY_PUBLIC": {
        "condition": lambda r, f: r.get("q7") == "FULL_BIRTHDAY",
        "category": "CAT_B",
        "severity": "CRITICAL",
        "title": "Full Birth Date (Day, Month, Year) Exposed",
        "description": "You reported displaying your complete birth date on your profile.",
        "technical_impact": "Full birth dates form a cornerstone of identity theft, credit bureau impersonation, and answering security questions for banking or healthcare accounts."
    },
    "FIND_EMAIL_PUBLIC": {
        "condition": lambda r, f: r.get("q6") == "YES",
        "category": "CAT_B",
        "severity": "HIGH",
        "title": "Personal Email Address Publicly Exposed",
        "description": "Your personal email address is publicly visible on your profile.",
        "technical_impact": "Enables automated email scraping bots, tailored spear-phishing campaigns, and credential stuffing attacks against linked portals."
    },
    "FIND_HOME_ADDRESS": {
        "condition": lambda r, f: r.get("q8") == "YES",
        "category": "CAT_B",
        "severity": "CRITICAL",
        "title": "Home Address or Exact Residential Neighborhood Disclosed",
        "description": "Granular residential location details are visible on your profile.",
        "technical_impact": "Destroys physical privacy, exposing the user to physical reconnaissance, harassment, and property record correlation."
    },
    "FIND_FAMILY_PUBLIC": {
        "condition": lambda r, f: r.get("q9") == "YES",
        "category": "CAT_B",
        "severity": "MEDIUM",
        "title": "Family Relationships & Dependents Explicitly Mapped",
        "description": "Family members and relationship links are publicly tagged.",
        "technical_impact": "Provides threat actors with mother's maiden names, siblings' names, and family context exploited in emergency caller/bail scams."
    },

    # Authentication & Account Security
    "FIND_MFA_DISABLED": {
        "condition": lambda r, f: r.get("q27") == "DISABLED",
        "category": "CAT_G",
        "severity": "CRITICAL",
        "title": "Multi-Factor Authentication (MFA) Disabled",
        "description": "Your account relies solely on single-factor password authentication.",
        "technical_impact": "Single-factor accounts have zero defense against credential stuffing or data breaches leaking password hashes."
    },
    "FIND_MFA_SMS_ONLY": {
        "condition": lambda r, f: r.get("q27") == "SMS_ONLY",
        "category": "CAT_G",
        "severity": "MEDIUM",
        "title": "MFA Relies Exclusively on Insecure SMS Codes",
        "description": "You use SMS text messages for two-factor authentication instead of an authenticator app.",
        "technical_impact": "SMS codes can be intercepted via SIM-swapping, SS7 telecom vulnerabilities, or social engineering against telecom telcos."
    },
    "FIND_PASSWORD_REUSE": {
        "condition": lambda r, f: r.get("q28") in ["REUSED", "SLIGHT_VARIATION"],
        "category": "CAT_G",
        "severity": "HIGH",
        "title": "Password Reuse or Predictable Variations Reported",
        "description": "The password used for this social account is shared or slightly modified from other websites.",
        "technical_impact": "A breach at any unrelated third-party website gives automated bots direct access to hijack this account."
    },
    "FIND_LOGIN_ALERTS_OFF": {
        "condition": lambda r, f: r.get("q30") in ["NO", "NOT_SURE"],
        "category": "CAT_G",
        "severity": "MEDIUM",
        "title": "Unrecognized Login Alerts Disabled or Unconfirmed",
        "description": "Real-time notifications for unrecognized logins from new devices or unknown locations are not verified.",
        "technical_impact": "Compromised accounts can be accessed and controlled without immediate defender detection."
    },
    "FIND_STALE_SESSIONS": {
        "condition": lambda r, f: r.get("q31") in ["NEVER", "RARELY"],
        "category": "CAT_G",
        "severity": "MEDIUM",
        "title": "Active Logged-In Sessions Rarely or Never Audited",
        "description": "No routine review of active session tokens across old phones, workstations, or borrowed computers.",
        "technical_impact": "Persistent session cookies remain valid for months, allowing physical or token-theft hijacking."
    },

    # Location Privacy
    "FIND_REALTIME_LOCATION": {
        "condition": lambda r, f: r.get("q10") in ["YES", "SOMETIMES"],
        "category": "CAT_C",
        "severity": "CRITICAL",
        "title": "Real-Time Location Broadcasts Enabled",
        "description": "You broadcast real-time location stamps or live geolocation feeds.",
        "technical_impact": "Allows real-world physical tracking, reveals exact coordinates in real-time, and confirms absence from your primary residence."
    },
    "FIND_INSTANT_CHECKINS": {
        "condition": lambda r, f: r.get("q11") == "IMMEDIATELY",
        "category": "CAT_C",
        "severity": "HIGH",
        "title": "Immediate Venue Check-ins Published While Present",
        "description": "You publish check-ins at public venues while still physically located at the establishment.",
        "technical_impact": "Broadcasts exact physical whereabouts to any observer before you can safely depart."
    },
    "FIND_ADVANCE_TRAVEL_PLANS": {
        "condition": lambda r, f: r.get("q12") in ["YES", "SOMETIMES"],
        "category": "CAT_C",
        "severity": "HIGH",
        "title": "Upcoming Travel Plans and Vacations Announced in Advance",
        "description": "Travel dates, airport itineraries, or vacation countdowns are shared publicly prior to trip conclusion.",
        "technical_impact": "Signals to threat actors and local burglars exactly when your home will be unoccupied."
    },
    "FIND_ROUTINE_TRACKING": {
        "condition": lambda r, f: r.get("q13") in ["YES", "SOMETIMES"],
        "category": "CAT_C",
        "severity": "HIGH",
        "title": "Predictable Daily Routines and Routes Exposed",
        "description": "Daily workout routes, recurring gym schedules, or commute paths are frequently posted.",
        "technical_impact": "Enables pattern-of-life analysis and predictable physical interception opportunities."
    },
    "FIND_EXIF_GEOTAGGING": {
        "condition": lambda r, f: r.get("q14") in ["YES", "NOT_SURE"],
        "category": "CAT_C",
        "severity": "MEDIUM",
        "title": "Camera GPS Geotagging Enabled on Photos",
        "description": "Photos may retain embedded EXIF GPS coordinates when captured or exported.",
        "technical_impact": "If uploaded to uncompressed platforms or shared directly, high-resolution EXIF coordinates reveal home and work locations."
    },

    # Profile Visibility
    "FIND_PROFILE_PUBLIC": {
        "condition": lambda r, f: r.get("q1") == "PUBLIC",
        "category": "CAT_A",
        "severity": "HIGH",
        "title": "Account Fully Publicly Accessible",
        "description": "Your entire profile and timeline are accessible to any anonymous internet user.",
        "technical_impact": "Greatly expands passive OSINT reconnaissance surface area and indexing by third-party identity search engines."
    },
    "FIND_SEARCH_INDEXING": {
        "condition": lambda r, f: r.get("q2") in ["YES", "NOT_SURE"],
        "category": "CAT_A",
        "severity": "MEDIUM",
        "title": "Profile Indexed by External Search Engines",
        "description": "Public search engines (Google, Bing) cache and index your profile link and summary.",
        "technical_impact": "Historical records and snippet caches remain searchable even if post privacy is later tightened."
    },
    "FIND_FRIENDS_LIST_PUBLIC": {
        "condition": lambda r, f: r.get("q3") == "PUBLIC",
        "category": "CAT_A",
        "severity": "HIGH",
        "title": "Friends and Followers List Publicly Exposed",
        "description": "Anyone can view and scrape your complete list of personal and professional connections.",
        "technical_impact": "Attackers can map your trust network to launch high-fidelity social engineering against your contacts."
    },

    # Tagging & Mentions
    "FIND_TAG_REVIEW_OFF": {
        "condition": lambda r, f: r.get("q23") in ["NO", "NOT_SURE"],
        "category": "CAT_F",
        "severity": "HIGH",
        "title": "Tag Review and Approval Disabled",
        "description": "Tagged posts, photos, and check-ins appear automatically on your timeline without prior consent.",
        "technical_impact": "Third parties can expose your private whereabouts, acquaintances, or sensitive activities without your consent."
    },
    "FIND_UNRESTRICTED_TAGGING": {
        "condition": lambda r, f: r.get("q24") == "EVERYONE",
        "category": "CAT_F",
        "severity": "MEDIUM",
        "title": "Unrestricted Tagging Permissions",
        "description": "Anyone on the platform is permitted to tag you in posts or images.",
        "technical_impact": "Exposes your account to tag-spam campaigns, crypto scam promotions, and unsolicited association."
    },

    # Friends & Connection Controls
    "FIND_UNKNOWN_CONNECTIONS": {
        "condition": lambda r, f: r.get("q19") in ["ACCEPT_MOST", "SOMETIMES"],
        "category": "CAT_E",
        "severity": "HIGH",
        "title": "Connection Requests from Unverified Strangers Accepted",
        "description": "You report accepting friend or follow requests from unfamiliar profiles with no known connection.",
        "technical_impact": "Allows adversary sockpuppet accounts inside your 'Friends-Only' privacy perimeter."
    },
    "FIND_NO_CONNECTION_AUDIT": {
        "condition": lambda r, f: r.get("q20") in ["NEVER", "RARELY"],
        "category": "CAT_E",
        "severity": "LOW",
        "title": "Stale Connections Never Audited",
        "description": "No routine review of existing connections or removal of dormant/compromised accounts.",
        "technical_impact": "Hacked legacy accounts among friends remain inside your trusted network."
    },

    # Content & Posts
    "FIND_POSTS_DEFAULT_PUBLIC": {
        "condition": lambda r, f: r.get("q15") == "PUBLIC",
        "category": "CAT_D",
        "severity": "HIGH",
        "title": "Default Post Audience Set to Public",
        "description": "All future posts are broadcast publicly unless manually restricted during authoring.",
        "technical_impact": "High rate of accidental personal data exposure due to default open visibility."
    },
    "FIND_SENSITIVE_DOCS": {
        "condition": lambda r, f: r.get("q16") in ["YES", "SOMETIMES"],
        "category": "CAT_D",
        "severity": "CRITICAL",
        "title": "Boarding Passes, Badges, or Work Desks Photographed",
        "description": "Photos show corporate badges, flight booking barcodes, or workstation monitors.",
        "technical_impact": "Barcodes leak PNRs and passport numbers; visible monitors leak internal company applications or credentials."
    },
    "FIND_SECURITY_ANSWER_LEAKS": {
        "condition": lambda r, f: r.get("q18") in ["YES", "SOMETIMES"],
        "category": "CAT_D",
        "severity": "HIGH",
        "title": "Participation in Viral Nostalgia / Security-Question Trends",
        "description": "Participated in viral questionnaire posts (e.g. first car, childhood street, pet name).",
        "technical_impact": "Publicly reveals common password reset security question answers to OSINT investigators."
    },

    # Third-Party Apps
    "FIND_THIRD_PARTY_UNREVIEWED": {
        "condition": lambda r, f: r.get("q33") in ["NEVER", "RARELY"],
        "category": "CAT_H",
        "severity": "HIGH",
        "title": "Third-Party App Access Tokens Never Audited",
        "description": "No periodic revocation of connected third-party OAuth apps and integrations.",
        "technical_impact": "Dormant third-party apps retain API permissions to read profile data, inbox, or contact graphs."
    },
    "FIND_OVERPRIVILEGED_APPS": {
        "condition": lambda r, f: r.get("q34") in ["YES", "NOT_SURE"],
        "category": "CAT_H",
        "severity": "HIGH",
        "title": "Third-Party Apps Granted Broad or Unverified Permissions",
        "description": "External apps hold permissions to read private messages, friend lists, or publish posts.",
        "technical_impact": "Supply chain compromise of any connected app exposes private social media account assets."
    },

    # Social Engineering & Messaging
    "FIND_SUSPICIOUS_LINK_RISK": {
        "condition": lambda r, f: r.get("q36") in ["CLICK_IMMEDIATELY", "INSPECT_URL"],
        "category": "CAT_I",
        "severity": "CRITICAL",
        "title": "High Vulnerability to Urgency-Based Phishing DMs",
        "description": "Likely to click unexpected links sent via DMs with sensational claims.",
        "technical_impact": "Directly vulnerable to credential harvesting phishing kits, session hijacking, or browser malware."
    },
    "FIND_OTP_SHARING_RISK": {
        "condition": lambda r, f: r.get("q37") in ["YES_HELP", "HESITATE"],
        "category": "CAT_I",
        "severity": "CRITICAL",
        "title": "Risk of Disclosing MFA Verification Codes Upon Request",
        "description": "Willingness to forward temporary verification codes sent to your phone or email.",
        "technical_impact": "Guarantees complete account takeover when an attacker initiates an automated password reset."
    },

    # Digital Footprint
    "FIND_OLD_POSTS_UNAUDITED": {
        "condition": lambda r, f: r.get("q40") in ["NEVER", "RARELY"],
        "category": "CAT_J",
        "severity": "MEDIUM",
        "title": "Years of Historical Public Posts Left Unaudited",
        "description": "Past posts from 3+ years ago remain publicly searchable without archiving.",
        "technical_impact": "Historical posts provide extensive personal timeline context used in credential recovery and profiling."
    },
    "FIND_ABANDONED_ACCOUNTS": {
        "condition": lambda r, f: r.get("q41") in ["YES_MULTIPLE", "MAYBE_ONE"],
        "category": "CAT_J",
        "severity": "HIGH",
        "title": "Dormant / Abandoned Social Accounts Left Online",
        "description": "Old social accounts with forgotten passwords remain active on legacy platforms.",
        "technical_impact": "Dormant accounts are easy targets for silent takeover and reputation poisoning."
    },
    "FIND_HANDLE_REUSE": {
        "condition": lambda r, f: r.get("q42") in ["SAME_EVERYWHERE", "SOME_OVERLAP"],
        "category": "CAT_J",
        "severity": "MEDIUM",
        "title": "Identical Handle Reused Across All Platforms",
        "description": "The exact same username is used across social, gaming, forums, and professional networks.",
        "technical_impact": "Allows rapid cross-platform correlation using automated OSINT recon scripts (e.g. Sherlock)."
    }
}

SEVERITY_ORDER = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}

def generate_privacy_findings(
    features: Dict[str, Any], 
    responses: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    Evaluates questionnaire responses against the finding definition rule base
    and returns a sorted list of concrete privacy findings.
    """
    findings: List[Dict[str, Any]] = []

    for fid, defn in FINDING_DEFINITIONS.items():
        if defn["condition"](responses, features):
            findings.append({
                "finding_id": fid,
                "category": defn["category"],
                "severity": defn["severity"],
                "title": defn["title"],
                "description": defn["description"],
                "technical_impact": defn["technical_impact"]
            })

    # Sort findings by severity (CRITICAL -> HIGH -> MEDIUM -> LOW)
    findings.sort(key=lambda x: SEVERITY_ORDER.get(x["severity"], 0), reverse=True)
    return findings
