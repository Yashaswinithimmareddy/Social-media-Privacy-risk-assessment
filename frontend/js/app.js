/**
 * Social Media Privacy Risk Assessment Framework
 * Shared Frontend JavaScript Utilities & API Client
 */

const API_BASE = "/api";

// Fetch wrapper with error handling
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                "Content-Type": "application/json",
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.error || `HTTP error ${response.status}`);
        }

        return await response.json();
    } catch (err) {
        console.error(`API Error on ${endpoint}:`, err);
        throw err;
    }
}

// Risk badge helper
function getRiskBadge(level) {
    const lvl = (level || "LOW").toUpperCase();
    let badgeClass = "badge-low";
    if (lvl === "MODERATE") badgeClass = "badge-moderate";
    else if (lvl === "HIGH") badgeClass = "badge-high";
    else if (lvl === "CRITICAL") badgeClass = "badge-critical";

    return `<span class="badge ${badgeClass}">${lvl}</span>`;
}

// Toast notification
function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `callout callout-${type}`;
    toast.style.position = "fixed";
    toast.style.bottom = "20px";
    toast.style.right = "20px";
    toast.style.zIndex = "9999";
    toast.style.maxWidth = "400px";
    toast.style.boxShadow = "0 10px 25px rgba(0,0,0,0.5)";
    toast.textContent = message;

    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.transition = "opacity 0.4s ease";
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}
