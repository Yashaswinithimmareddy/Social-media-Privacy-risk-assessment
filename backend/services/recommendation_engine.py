"""
Social Media Privacy Risk Assessment Framework
Security Recommendation Engine

Translates detected privacy findings into prioritized, actionable security hardening
guidance categorized by urgency: IMMEDIATE, IMPORTANT, and GOOD PRACTICE.
"""

from typing import List, Dict, Any

RECOMMENDATION_CATALOG = {
    "FIND_PHONE_PUBLIC": {
        "priority": "IMMEDIATE",
        "action": "Remove or strictly hide your mobile phone number from all public profiles.",
        "step_by_step": "Navigate to Account Settings -> Personal Information -> Contact Info -> Set Phone Visibility to 'Only Me' or remove it from public display.",
        "risk_reduction_impact": "High (Protects against SIM swapping, smishing, and identity correlation)"
    },
    "FIND_BIRTHDAY_PUBLIC": {
        "priority": "IMMEDIATE",
        "action": "Hide your birth year or privatize your full date of birth completely.",
        "step_by_step": "Go to Edit Profile -> Basic Info -> Birthday -> Toggle Birth Year to 'Only Me' or hide the entire date.",
        "risk_reduction_impact": "High (Eliminates a primary data point used in financial identity theft and account resets)"
    },
    "FIND_MFA_DISABLED": {
        "priority": "IMMEDIATE",
        "action": "Enable Multi-Factor Authentication (MFA) immediately using a mobile authenticator app.",
        "step_by_step": "Go to Settings -> Security & Login -> Two-Factor Authentication -> Choose 'Authentication App' (e.g. Google Authenticator, Bitwarden, or 1Password) and save backup codes.",
        "risk_reduction_impact": "Critical (Blocks over 90% of automated credential stuffing attacks)"
    },
    "FIND_PASSWORD_REUSE": {
        "priority": "IMMEDIATE",
        "action": "Change your password to a unique 16+ character passphrase managed by a password manager.",
        "step_by_step": "Use an encrypted password manager to generate a unique random password. Change it immediately under Security Settings.",
        "risk_reduction_impact": "Critical (Shields account from credential stuffing attacks caused by third-party data breaches)"
    },
    "FIND_REALTIME_LOCATION": {
        "priority": "IMMEDIATE",
        "action": "Disable real-time location sharing and avoid live venue updates.",
        "step_by_step": "Turn off device-level location access for the social media app in Phone Settings -> Privacy -> Location Services. Stop broadcasting live stories.",
        "risk_reduction_impact": "High (Eliminates physical surveillance and home vacancy signaling)"
    },
    "FIND_SENSITIVE_DOCS": {
        "priority": "IMMEDIATE",
        "action": "Review and delete photos showing boarding passes, ID badges, or workplace computer screens.",
        "step_by_step": "Search your photo timeline for travel and work photos. Delete or archive posts with visible barcodes, badges, or monitors.",
        "risk_reduction_impact": "Critical (Prevents airline record hijacking and corporate espionage)"
    },
    "FIND_OTP_SHARING_RISK": {
        "priority": "IMMEDIATE",
        "action": "Never disclose one-time passwords (OTPs) or verification codes to anyone under any condition.",
        "step_by_step": "Remember: Platform staff, friends, or family will NEVER legitimately ask for your 6-digit MFA code. Any request is a direct takeover attempt.",
        "risk_reduction_impact": "Critical (Prevents direct session and account takeover)"
    },
    "FIND_HOME_ADDRESS": {
        "priority": "IMMEDIATE",
        "action": "Remove residential street address, apartment number, or specific neighborhood from your bio.",
        "step_by_step": "Edit Profile -> Places Lived -> Remove specific residential entries or set to general region only.",
        "risk_reduction_impact": "High (Preserves physical home safety and prevents stalking)"
    },
    "FIND_EMAIL_PUBLIC": {
        "priority": "IMPORTANT",
        "action": "Set personal email address visibility to 'Only Me' or use an alias.",
        "step_by_step": "Account Settings -> Contact Info -> Set primary email to private. Use an email relay alias for public contact if needed.",
        "risk_reduction_impact": "Moderate (Reduces spam, phishing, and credential stuffing vectors)"
    },
    "FIND_TAG_REVIEW_OFF": {
        "priority": "IMPORTANT",
        "action": "Enable Tag Review and Timeline Approval.",
        "step_by_step": "Settings -> Profile and Tagging -> Enable 'Review posts that you're tagged in before the post appears on your profile'.",
        "risk_reduction_impact": "Moderate (Prevents non-consensual location and association exposure)"
    },
    "FIND_UNKNOWN_CONNECTIONS": {
        "priority": "IMPORTANT",
        "action": "Adopt a strict 'Verify Before Accepting' policy for incoming connection requests.",
        "step_by_step": "Reject requests from empty profiles or strangers. Verify questionable requests out-of-band before accepting.",
        "risk_reduction_impact": "Moderate (Keeps adversary sockpuppets outside your private network perimeter)"
    },
    "FIND_THIRD_PARTY_UNREVIEWED": {
        "priority": "IMPORTANT",
        "action": "Audit connected third-party apps and revoke permissions for unused integrations.",
        "step_by_step": "Settings -> Apps and Websites -> Review active connections -> Revoke access for any app unused in the past 90 days.",
        "risk_reduction_impact": "Moderate (Enforces Principle of Least Privilege across OAuth integrations)"
    },
    "FIND_OVERPRIVILEGED_APPS": {
        "priority": "IMPORTANT",
        "action": "Revoke excessive OAuth permissions granted to third-party tools.",
        "step_by_step": "In the connected apps management menu, remove apps requesting inbox or post-publishing permissions.",
        "risk_reduction_impact": "Moderate (Minimizes third-party data collection reach)"
    },
    "FIND_SUSPICIOUS_LINK_RISK": {
        "priority": "IMPORTANT",
        "action": "Treat unexpected links in direct messages with extreme suspicion.",
        "step_by_step": "Never click sensationalized DM links. Confirm with the sender through an alternate channel (phone call or text).",
        "risk_reduction_impact": "High (Prevents drive-by credential harvesting and malware infection)"
    },
    "FIND_ADVANCE_TRAVEL_PLANS": {
        "priority": "IMPORTANT",
        "action": "Adopt delayed vacation posting: share trip highlights only after returning home.",
        "step_by_step": "Store photos locally during travel. Publish albums and stories after you are back in your residence.",
        "risk_reduction_impact": "Moderate (Eliminates vacant home exploitation)"
    },
    "FIND_INSTANT_CHECKINS": {
        "priority": "IMPORTANT",
        "action": "Wait until departing a restaurant or venue before checking in.",
        "step_by_step": "Check-ins posted in real-time pinpoint your exact seat or table. Post retroactively.",
        "risk_reduction_impact": "Moderate (Enhances physical security)"
    },
    "FIND_LOGIN_ALERTS_OFF": {
        "priority": "IMPORTANT",
        "action": "Turn on alerts for unrecognized logins from new devices.",
        "step_by_step": "Settings -> Security -> Get alerts about unrecognized logins -> Enable Email and Notification alerts.",
        "risk_reduction_impact": "Moderate (Provides early breach notification)"
    },
    "FIND_FRIENDS_LIST_PUBLIC": {
        "priority": "IMPORTANT",
        "action": "Change friend/follower list visibility to 'Only Me'.",
        "step_by_step": "Privacy Settings -> 'Who can see your friends list?' -> Change from Public to 'Only Me'.",
        "risk_reduction_impact": "Moderate (Prevents contact scraping and executive impersonation)"
    },
    "FIND_PROFILE_PUBLIC": {
        "priority": "IMPORTANT",
        "action": "Consider restricting default profile visibility or enabling privacy lock.",
        "step_by_step": "Settings -> Privacy -> Profile Locking -> Enable Private Profile mode.",
        "risk_reduction_impact": "High (Restricts overall OSINT exposure)"
    },
    "FIND_SEARCH_INDEXING": {
        "priority": "GOOD PRACTICE",
        "action": "Opt out of external search engine indexing.",
        "step_by_step": "Privacy Settings -> 'Do you want search engines outside of the platform to link to your profile?' -> Toggle to 'No'.",
        "risk_reduction_impact": "Low to Moderate (Limits search engine crawler caching)"
    },
    "FIND_OLD_POSTS_UNAUDITED": {
        "priority": "GOOD PRACTICE",
        "action": "Run a historical post audit using the platform's 'Limit Past Posts' tool.",
        "step_by_step": "Privacy Settings -> 'Limit the audience for old posts' -> Click 'Limit Past Posts' to mass-convert public posts to Friends-Only.",
        "risk_reduction_impact": "Moderate (Removes years of legacy digital footprint data)"
    },
    "FIND_ABANDONED_ACCOUNTS": {
        "priority": "GOOD PRACTICE",
        "action": "Delete or secure dormant accounts on platforms you no longer use.",
        "step_by_step": "Log in to old accounts, export any photos you wish to keep, and permanently request account deletion.",
        "risk_reduction_impact": "Moderate (Reduces passive attack surface and credential exposure)"
    },
    "FIND_HANDLE_REUSE": {
        "priority": "GOOD PRACTICE",
        "action": "Decouple usernames between professional, gaming, and personal accounts.",
        "step_by_step": "Use unique pseudonyms for non-professional accounts to prevent automated OSINT linkage.",
        "risk_reduction_impact": "Low (Complicates adversary reconnaissance across different platforms)"
    },
    "FIND_MFA_SMS_ONLY": {
        "priority": "GOOD PRACTICE",
        "action": "Upgrade from SMS verification to an Authenticator App (TOTP) or FIDO2 Security Key.",
        "step_by_step": "Add Google Authenticator or Microsoft Authenticator in Security settings, then disable SMS delivery.",
        "risk_reduction_impact": "Moderate (Eliminates SIM-swap interception risks)"
    },
    "FIND_FAMILY_PUBLIC": {
        "priority": "GOOD PRACTICE",
        "action": "Remove explicit family tags and relationship linkages from public bio.",
        "step_by_step": "Edit Profile -> Relationship and Family -> Set visibility to 'Only Me'.",
        "risk_reduction_impact": "Low (Protects security question answers)"
    },
    "FIND_UNRESTRICTED_TAGGING": {
        "priority": "GOOD PRACTICE",
        "action": "Restrict who can tag you to 'Friends Only' or require manual approval.",
        "step_by_step": "Settings -> Profile and Tagging -> 'Who can tag you?' -> Change to Friends.",
        "risk_reduction_impact": "Low (Reduces spam notifications and crypto tagging)"
    },
    "FIND_ROUTINE_TRACKING": {
        "priority": "GOOD PRACTICE",
        "action": "Vary posting schedules and avoid sharing exact gym or running routes.",
        "step_by_step": "Crop route maps from fitness tracker posts and blur out identifiable street names.",
        "risk_reduction_impact": "Moderate (Protects daily physical schedule)"
    },
    "FIND_EXIF_GEOTAGGING": {
        "priority": "GOOD PRACTICE",
        "action": "Disable camera location tags on your mobile smartphone.",
        "step_by_step": "Device Camera Settings -> Save Location / Geotagging -> Toggle Off.",
        "risk_reduction_impact": "Moderate (Stops GPS coordinate leakage in original image files)"
    },
    "FIND_POSTS_DEFAULT_PUBLIC": {
        "priority": "GOOD PRACTICE",
        "action": "Change default post audience from Public to Friends or Restricted List.",
        "step_by_step": "Settings -> Privacy -> 'Who can see your future posts?' -> Select 'Friends'.",
        "risk_reduction_impact": "Moderate (Creates a safe default posture for future activity)"
    },
    "FIND_SECURITY_ANSWER_LEAKS": {
        "priority": "GOOD PRACTICE",
        "action": "Avoid participating in viral nostalgia surveys asking for first pets, childhood schools, or mothers' maiden names.",
        "step_by_step": "Recognize that nostalgic viral challenges are often intelligence-gathering lures. Delete past responses.",
        "risk_reduction_impact": "Moderate (Protects account recovery questions)"
    },
    "FIND_NO_CONNECTION_AUDIT": {
        "priority": "GOOD PRACTICE",
        "action": "Perform a biannual connections spring-cleaning.",
        "step_by_step": "Scroll through your friends list and unfriend or unfollow people you do not recognize or interact with.",
        "risk_reduction_impact": "Low (Maintains a clean and trusted circle)"
    },
    "FIND_STALE_SESSIONS": {
        "priority": "GOOD PRACTICE",
        "action": "Inspect active sessions and click 'Log Out of All Other Sessions'.",
        "step_by_step": "Settings -> Security & Login -> 'Where you're logged in' -> Review and terminate unfamiliar or older sessions.",
        "risk_reduction_impact": "Moderate (Revokes stale authentication tokens)"
    }
}

PRIORITY_SORT = {"IMMEDIATE": 3, "IMPORTANT": 2, "GOOD PRACTICE": 1}

def generate_recommendations(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generates personalized recommendations based on detected findings,
    sorted by urgency level (IMMEDIATE -> IMPORTANT -> GOOD PRACTICE).
    """
    recommendations: List[Dict[str, Any]] = []

    for finding in findings:
        fid = finding["finding_id"]
        cat = RECOMMENDATION_CATALOG.get(fid)
        if cat:
            recommendations.append({
                "recommendation_id": f"REC_{fid}",
                "finding_id": fid,
                "finding_title": finding["title"],
                "category": finding["category"],
                "priority": cat["priority"],
                "action": cat["action"],
                "step_by_step": cat["step_by_step"],
                "risk_reduction_impact": cat["risk_reduction_impact"]
            })

    # Sort by priority
    recommendations.sort(key=lambda x: PRIORITY_SORT.get(x["priority"], 0), reverse=True)
    return recommendations
