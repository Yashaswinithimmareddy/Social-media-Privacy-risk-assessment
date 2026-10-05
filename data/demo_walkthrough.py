"""
Social Media Privacy Risk Assessment Framework
Safe Demonstration Profile Walkthrough & Before/After Simulation

Executes the designated cybersecurity demonstration profile:
1. Baseline Insecure/High-Exposure Profile
2. Risk Findings & Category Analysis
3. Hardening Simulation (-50+ point drop)
4. Exports JSON and HTML report artifacts to reports/
"""

import os
import sys
import json

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.services.assessment_engine import run_assessment
from backend.services.improvement_simulator import simulate_privacy_improvement
from backend.models.database import save_assessment, init_db

REPORTS_DIR = os.path.join(project_root, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def run_demo():
    print("=" * 70)
    print("DEMO PROFILE: HIGH-EXPOSURE SOCIAL MEDIA ACCOUNT ASSESSMENT")
    print("=" * 70)

    # 1. Configured responses as specified in section 32
    demo_responses = {
        "q1": "PUBLIC",                 # Profile: Public
        "q2": "YES",                    # Search indexing: Yes
        "q3": "PUBLIC",                 # Friends list: Public
        "q4": "PUBLIC",                 # Profile photo: Public
        "q5": "YES",                    # Phone: Public
        "q6": "NO",                     # Email: Private
        "q7": "FULL_BIRTHDAY",          # Full Birthday: Public
        "q8": "YES",                    # Home location: Public
        "q9": "YES",                    # Family: Public
        "q10": "YES",                   # Real-time Location: Yes
        "q11": "IMMEDIATELY",           # Real-Time Check-ins: Yes
        "q12": "YES",                   # Travel Plans: Public
        "q13": "YES",                   # Daily Routine: Public
        "q14": "YES",                   # Geotagging: Yes
        "q15": "PUBLIC",                # Posts: Public
        "q16": "YES",                   # Badge/Boarding pass: Yes
        "q17": "YES",                   # Minors: Yes
        "q18": "YES",                   # Nostalgia quiz: Yes
        "q19": "ACCEPT_MOST",           # Unknown Requests: Often Accepted
        "q20": "NEVER",                 # Connection audit: Never
        "q21": "NEVER",                 # Restricted lists: Never
        "q22": "ANYONE",                # Messages: Anyone
        "q23": "NO",                    # Tag Review: Disabled
        "q24": "EVERYONE",              # Tagging: Everyone
        "q25": "ENABLED",               # Face recognition: Enabled
        "q26": "EVERYONE",              # Mentions: Everyone
        "q27": "DISABLED",              # MFA: Disabled
        "q28": "REUSED",                # Password reuse: Reused
        "q29": "NO",                    # Password manager: No
        "q30": "NO",                    # Login Alerts: Disabled
        "q31": "NEVER",                 # Session audit: Never
        "q32": "FREQUENTLY",            # Social logins: Frequent
        "q33": "NEVER",                 # Third-Party Apps: Not Reviewed
        "q34": "YES",                   # Excessive app permissions: Yes
        "q35": "YES",                   # Quizzes: Yes
        "q36": "CLICK_IMMEDIATELY",     # Phishing link: Clicks
        "q37": "YES_HELP",              # OTP: Shares
        "q38": "TRUST_URGENCY",         # Impersonation: Trusts
        "q39": "ENGAGE_OFTEN",          # Scam giveaways: Engages
        "q40": "NEVER",                 # Old Posts: Not Reviewed
        "q41": "YES_MULTIPLE",          # Dormant accounts: Multiple
        "q42": "SAME_EVERYWHERE",       # Handle reuse: Same
        "q43": "NEVER",                 # Privacy audit: Never
        "q44": "NEVER"                  # Data archive: Never
    }

    # Execute Assessment
    result = run_assessment(demo_responses)
    init_db()
    save_assessment(result)

    print(f"\n[+] ASSESSMENT GENERATED: {result['assessment_id']}")
    print(f"[*] Overall Privacy Risk Score : {result['overall_score']} / 100")
    print(f"[*] Risk Classification        : {result['risk_level']}")
    print("\n--- CATEGORY-WISE EXPOSURE SCORES ---")
    for cat_id, cat_data in result["category_scores"].items():
        print(f"  * {cat_data['name']:<35}: {cat_data['score']:>5.1f} / 100  [{cat_data['risk_level']}]")

    print(f"\n--- DETECTED CRITICAL & HIGH FINDINGS ({len(result['findings'])} total) ---")
    for i, finding in enumerate(result["findings"][:6], 1):
        print(f"  {i}. [{finding['severity']}] {finding['title']}")
        print(f"     Impact: {finding['technical_impact']}")

    print(f"\n--- TOP PRIORITIZED RECOMMENDATIONS ({len(result['recommendations'])} total) ---")
    for i, rec in enumerate(result["recommendations"][:5], 1):
        print(f"  {i}. [{rec['priority']}] {rec['action']}")
        print(f"     Remediation: {rec['step_by_step']}")

    # 2. Execute Improvement Simulation
    print("\n" + "=" * 70)
    print("SIMULATING DEFENSIVE HARDENING ACTIONS:")
    print("  [X] Phone Number      -> Private (Hidden)")
    print("  [X] Full Birth Date   -> Private (Hidden)")
    print("  [X] Real-Time Loc     -> Disabled")
    print("  [X] Check-ins         -> Delayed (After Leaving)")
    print("  [X] Unknown Requests  -> Reject Strangers")
    print("  [X] Tag Review        -> Enabled")
    print("  [X] Multi-Factor Auth -> Enabled (Authenticator App)")
    print("  [X] Password Hygiene  -> Unique Passwords Managed")
    print("  [X] Login Alerts      -> Enabled")
    print("  [X] Third-Party Apps  -> Audited Regularly")
    print("  [X] Historical Posts  -> Mass-Privatized")
    print("=" * 70)

    simulated_changes = [
        "make_phone_private",
        "hide_birth_year",
        "disable_realtime_location",
        "delay_venue_checkins",
        "restrict_unknown_connections",
        "enable_tag_review",
        "enable_mfa",
        "unique_password",
        "enable_login_alerts",
        "audit_third_party_apps",
        "limit_past_posts"
    ]

    sim_res = simulate_privacy_improvement(demo_responses, simulated_changes)

    base_score = sim_res["baseline"]["overall_score"]
    hardened_score = sim_res["simulated"]["overall_score"]
    diff = sim_res["points_reduced"]
    pct = sim_res["percentage_improvement"]

    print(f"\n[+] SIMULATION RESULTS:")
    print(f"    Baseline Risk Score : {base_score} ({sim_res['baseline']['risk_level']})")
    print(f"    Hardened Risk Score : {hardened_score} ({sim_res['simulated']['risk_level']})")
    print(f"    Net Risk Reduction  : -{diff} Points (-{pct}%)")
    print(f"\n[+] Status Shift: {sim_res['baseline']['risk_level']} ====> {sim_res['simulated']['risk_level']}")

    # 3. Export JSON report
    report_json_path = os.path.join(REPORTS_DIR, "demo_assessment_walkthrough.json")
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "assessment": result,
            "simulation": sim_res
        }, f, indent=2)
    print(f"\n[+] Exported JSON report: {report_json_path}")

    # 4. Export static HTML report
    html_report_path = os.path.join(REPORTS_DIR, "demo_assessment_report.html")
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Assessment Report - {result['assessment_id']}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0b0f19; color: #f9fafb; margin: 2rem auto; max-width: 900px; line-height: 1.6; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.75rem; text-transform: uppercase; }}
        .badge-critical {{ background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }}
        .badge-moderate {{ background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #f59e0b; }}
        .card {{ background: #111827; border: 1px solid #374151; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
        th, td {{ padding: 10px; border-bottom: 1px solid #374151; text-align: left; }}
        th {{ background: #1f2937; color: #9ca3af; }}
    </style>
</head>
<body>
    <div class="card">
        <h1 style="margin: 0; color: #06b6d4;">Social Media Privacy Risk Assessment Report</h1>
        <p style="color: #9ca3af; margin: 5px 0 20px 0;">Identifier: {result['assessment_id']} | Date: {result['created_at']}</p>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2>Overall Risk Score: <span style="color: #ef4444;">{result['overall_score']} / 100</span></h2>
                <div>Classification: <span class="badge badge-critical">{result['risk_level']}</span></div>
            </div>
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; padding: 15px; border-radius: 8px; text-align: right;">
                <div style="font-size: 0.8rem; color: #9ca3af;">Simulated Score After 11 Controls:</div>
                <div style="font-size: 1.6rem; font-weight: bold; color: #10b981;">{hardened_score} / 100 (-{diff} pts)</div>
                <div style="font-size: 0.85rem; color: #34d399;">New Tier: {sim_res['simulated']['risk_level']}</div>
            </div>
        </div>
    </div>

    <div class="card">
        <h3>Category Breakdown</h3>
        <table>
            <tr><th>Category</th><th>Score</th><th>Tier</th></tr>
            {"".join(f"<tr><td>{c['name']}</td><td><strong>{c['score']}</strong>/100</td><td>{c['risk_level']}</td></tr>" for c in result['category_scores'].values())}
        </table>
    </div>

    <div class="card">
        <h3>Top Critical Findings</h3>
        {"".join(f"<div style='margin-bottom: 12px; border-left: 3px solid #ef4444; padding-left: 10px;'><strong>{f['title']}</strong><br><small style='color: #9ca3af;'>{f['technical_impact']}</small></div>" for f in result['findings'][:5])}
    </div>

    <div class="card">
        <h3>Prioritized Remediations</h3>
        {"".join(f"<div style='margin-bottom: 12px; border-left: 3px solid #10b981; padding-left: 10px;'><strong>[{r['priority']}] {r['action']}</strong><br><small style='color: #9ca3af;'>{r['step_by_step']}</small></div>" for r in result['recommendations'][:5])}
    </div>
</body>
</html>
"""
    with open(html_report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] Exported HTML report: {html_report_path}")

if __name__ == "__main__":
    run_demo()
