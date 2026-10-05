/**
 * Social Media Privacy Risk Assessment Framework
 * Simulator Controller
 */

let currentAssessmentId = null;
let baseResponses = null;

const SIMULATION_TOGGLES = [
    {
        key: "make_phone_private",
        label: "Make mobile phone number private / hidden",
        icon: "fa-phone-slash",
        category: "Personal Information",
        description: "Removes phone number from public display, preventing SIM-swapping and smishing.",
        checked: true
    },
    {
        key: "hide_birth_year",
        label: "Hide birth year or full birth date",
        icon: "fa-cake-candles",
        category: "Personal Information",
        description: "Protects date of birth used in credit fraud and security question bypass.",
        checked: true
    },
    {
        key: "disable_realtime_location",
        label: "Disable real-time location broadcasts",
        icon: "fa-location-crosshairs",
        category: "Location Privacy",
        description: "Stops broadcasting live presence and prevents home vacancy signaling.",
        checked: true
    },
    {
        key: "delay_venue_checkins",
        label: "Delay venue check-ins until after leaving",
        icon: "fa-clock",
        category: "Location Privacy",
        description: "Post check-ins retroactively so physical whereabouts are not pinpointed in real-time.",
        checked: false
    },
    {
        key: "enable_mfa",
        label: "Enable Multi-Factor Authentication (MFA / 2FA)",
        icon: "fa-key",
        category: "Authentication",
        description: "Enforces app-based TOTP or hardware security key, stopping credential stuffing.",
        checked: true
    },
    {
        key: "unique_password",
        label: "Use a unique high-entropy password",
        icon: "fa-shield-halved",
        category: "Authentication",
        description: "Breaks credential reuse linkage from third-party breached databases.",
        checked: false
    },
    {
        key: "enable_login_alerts",
        label: "Turn on unrecognized login alerts",
        icon: "fa-bell",
        category: "Authentication",
        description: "Receive instant email and push alerts whenever a new device connects.",
        checked: false
    },
    {
        key: "enable_tag_review",
        label: "Enable tag review before posts appear on profile",
        icon: "fa-tags",
        category: "Tagging & Mentions",
        description: "Require manual approval before tagged photos reveal your whereabouts.",
        checked: true
    },
    {
        key: "restrict_unknown_connections",
        label: "Reject or verify unknown connection requests",
        icon: "fa-user-shield",
        category: "Friends & Followers",
        description: "Keeps malicious reconnaissance sockpuppets outside your private network perimeter.",
        checked: false
    },
    {
        key: "audit_third_party_apps",
        label: "Audit and revoke unused third-party OAuth apps",
        icon: "fa-cubes",
        category: "Third-Party Apps",
        description: "Enforces Principle of Least Privilege across connected legacy services.",
        checked: false
    },
    {
        key: "limit_past_posts",
        label: "Mass-privatize historical public posts",
        icon: "fa-history",
        category: "Digital Footprint",
        description: "Restricts public visibility of old posts from 3+ years ago.",
        checked: false
    },
    {
        key: "verify_phishing_links",
        label: "Strict out-of-band verification for suspicious DMs",
        icon: "fa-envelope-circle-check",
        category: "Social Engineering",
        description: "Never click unexpected emotional links; confirm through alternative channels.",
        checked: false
    }
];

// Default high-exposure baseline if none supplied
const DEFAULT_HIGH_EXPOSURE_RESPONSES = {
    q1: "PUBLIC", q2: "YES", q3: "PUBLIC", q4: "PUBLIC",
    q5: "YES", q6: "YES", q7: "FULL_BIRTHDAY", q8: "YES", q9: "YES",
    q10: "YES", q11: "IMMEDIATELY", q12: "YES", q13: "YES", q14: "YES",
    q15: "PUBLIC", q16: "YES", q17: "YES", q18: "YES",
    q19: "ACCEPT_MOST", q20: "NEVER", q21: "NEVER", q22: "ANYONE",
    q23: "NO", q24: "EVERYONE", q25: "ENABLED", q26: "EVERYONE",
    q27: "DISABLED", q28: "REUSED", q29: "NO", q30: "NO", q31: "NEVER",
    q32: "FREQUENTLY", q33: "NEVER", q34: "YES", q35: "YES",
    q36: "CLICK_IMMEDIATELY", q37: "YES_HELP", q38: "TRUST_URGENCY", q39: "ENGAGE_OFTEN",
    q40: "NEVER", q41: "YES_MULTIPLE", q42: "SAME_EVERYWHERE", q43: "NEVER", q44: "NEVER"
};

document.addEventListener("DOMContentLoaded", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    currentAssessmentId = urlParams.get("id");

    if (currentAssessmentId) {
        try {
            const assessment = await apiRequest(`/assessment/${currentAssessmentId}`);
            baseResponses = assessment.cleaned_responses || DEFAULT_HIGH_EXPOSURE_RESPONSES;
        } catch (e) {
            baseResponses = DEFAULT_HIGH_EXPOSURE_RESPONSES;
        }
    } else {
        baseResponses = DEFAULT_HIGH_EXPOSURE_RESPONSES;
    }

    renderPresets();
    await runSimulation();
});

function renderPresets() {
    const container = document.getElementById("presets-container");
    container.innerHTML = SIMULATION_TOGGLES.map(preset => `
        <div class="card" style="padding: 1.25rem; display: flex; align-items: flex-start; gap: 1rem;">
            <input type="checkbox" id="chk-${preset.key}" value="${preset.key}" 
                   ${preset.checked ? 'checked' : ''} 
                   onchange="handleToggleChange()" 
                   style="margin-top: 0.35rem; width: 20px; height: 20px; accent-color: var(--accent-blue); cursor: pointer;">
            <div style="flex: 1;">
                <label for="chk-${preset.key}" style="font-weight: 600; font-size: 0.95rem; cursor: pointer; display: flex; align-items: center; gap: 0.5rem;">
                    <i class="fa-solid ${preset.icon}" style="color: var(--accent-cyan);"></i>
                    ${preset.label}
                </label>
                <div style="font-size: 0.75rem; color: var(--accent-blue); margin: 0.2rem 0;">${preset.category}</div>
                <div style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">${preset.description}</div>
            </div>
        </div>
    `).join("");
}

window.handleToggleChange = async function() {
    await runSimulation();
};

async function runSimulation() {
    const selected = [];
    SIMULATION_TOGGLES.forEach(p => {
        const chk = document.getElementById(`chk-${p.key}`);
        if (chk && chk.checked) {
            selected.push(p.key);
        }
    });

    try {
        const payload = {
            responses: baseResponses,
            improvements: selected
        };
        if (currentAssessmentId) {
            payload.assessment_id = currentAssessmentId;
        }

        const simResult = await apiRequest("/assessment/simulate-improvement", {
            method: "POST",
            body: JSON.stringify(payload)
        });

        // Update UI
        const baseScore = simResult.baseline.overall_score;
        const simScore = simResult.simulated.overall_score;
        const diff = simResult.points_reduced;
        const pct = simResult.percentage_improvement;

        document.getElementById("sim-baseline-score").textContent = baseScore.toFixed(1);
        document.getElementById("sim-baseline-badge").innerHTML = getRiskBadge(simResult.baseline.risk_level);

        document.getElementById("sim-hardened-score").textContent = simScore.toFixed(1);
        document.getElementById("sim-hardened-badge").innerHTML = getRiskBadge(simResult.simulated.risk_level);

        document.getElementById("sim-points-reduced").textContent = `- ${diff.toFixed(1)} Points`;
        document.getElementById("sim-percentage-improvement").textContent = `${pct.toFixed(1)}% Reduction`;

        // Update colors based on levels
        const hardenedElem = document.getElementById("sim-hardened-score");
        if (simScore <= 20) hardenedElem.style.color = "var(--risk-low)";
        else if (simScore <= 40) hardenedElem.style.color = "var(--risk-moderate)";
        else if (simScore <= 70) hardenedElem.style.color = "var(--risk-high)";
        else hardenedElem.style.color = "var(--risk-critical)";

    } catch (err) {
        console.error("Simulation error:", err);
    }
}
