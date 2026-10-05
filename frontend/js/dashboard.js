/**
 * Social Media Privacy Risk Assessment Framework
 * Dashboard Controller & Chart.js Visualizations
 */

document.addEventListener("DOMContentLoaded", async () => {
    await loadDashboardData();
});

async function loadDashboardData() {
    try {
        const stats = await apiRequest("/dashboard/stats");
        renderStatCards(stats);
        renderRadarChart(stats.category_averages);
        renderDonutChart(stats.risk_distribution);
        renderBarChart(stats.category_averages);
        renderWeaknessesChart(stats.top_findings);
        renderRecentTable(stats.recent_assessments);
    } catch (err) {
        console.error("Dashboard data load error:", err);
        showToast("Error loading dashboard metrics: " + err.message, "danger");
    }
}

function renderStatCards(stats) {
    document.getElementById("stat-total-assessments").textContent = stats.total_assessments.toLocaleString();
    document.getElementById("stat-avg-score").textContent = `${stats.average_risk_score}/100`;
    document.getElementById("stat-critical-count").textContent = stats.risk_distribution.CRITICAL || 0;
    document.getElementById("stat-low-count").textContent = stats.risk_distribution.LOW || 0;
}

function renderRadarChart(categoryAverages) {
    const ctx = document.getElementById("categoryRadarChart").getContext("2d");
    const labels = categoryAverages.map(c => c.name);
    const dataValues = categoryAverages.map(c => c.avg_score);

    new Chart(ctx, {
        type: "radar",
        data: {
            labels: labels,
            datasets: [{
                label: "Average Risk Score",
                data: dataValues,
                backgroundColor: "rgba(6, 182, 212, 0.25)",
                borderColor: "#06b6d4",
                borderWidth: 2,
                pointBackgroundColor: "#3b82f6",
                pointBorderColor: "#fff",
                pointHoverBackgroundColor: "#fff",
                pointHoverBorderColor: "#3b82f6"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: "rgba(255, 255, 255, 0.1)" },
                    grid: { color: "rgba(255, 255, 255, 0.1)" },
                    pointLabels: {
                        color: "#9ca3af",
                        font: { size: 10 }
                    },
                    ticks: {
                        backdropColor: "transparent",
                        color: "#6b7280",
                        stepSize: 20,
                        min: 0,
                        max: 100
                    }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderDonutChart(distribution) {
    const ctx = document.getElementById("riskDonutChart").getContext("2d");
    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Low Risk (0-20)", "Moderate (21-40)", "High (41-70)", "Critical (71-100)"],
            datasets: [{
                data: [
                    distribution.LOW || 0,
                    distribution.MODERATE || 0,
                    distribution.HIGH || 0,
                    distribution.CRITICAL || 0
                ],
                backgroundColor: [
                    "#10b981",  // Low
                    "#f59e0b",  // Moderate
                    "#f97316",  // High
                    "#ef4444"   // Critical
                ],
                borderColor: "#111827",
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { color: "#9ca3af", boxWidth: 12, padding: 15 }
                }
            },
            cutout: "68%"
        }
    });
}

function renderBarChart(categoryAverages) {
    const ctx = document.getElementById("categoryBarChart").getContext("2d");
    const labels = categoryAverages.map(c => c.name);
    const dataValues = categoryAverages.map(c => c.avg_score);

    // Color bars based on score severity
    const colors = dataValues.map(score => {
        if (score <= 20) return "#10b981";
        if (score <= 40) return "#f59e0b";
        if (score <= 70) return "#f97316";
        return "#ef4444";
    });

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Risk Score",
                data: dataValues,
                backgroundColor: colors,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: { color: "#9ca3af", font: { size: 9 }, maxRotation: 45, minRotation: 45 },
                    grid: { display: false }
                },
                y: {
                    min: 0,
                    max: 100,
                    ticks: { color: "#6b7280" },
                    grid: { color: "rgba(255, 255, 255, 0.05)" }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderWeaknessesChart(topFindings) {
    const ctx = document.getElementById("topWeaknessesChart").getContext("2d");
    const labels = (topFindings || []).map(f => f.title.length > 28 ? f.title.substring(0, 26) + "..." : f.title);
    const dataValues = (topFindings || []).map(f => f.frequency);

    new Chart(ctx, {
        type: "bar",
        indexAxis: "y",
        data: {
            labels: labels,
            datasets: [{
                label: "Detection Frequency",
                data: dataValues,
                backgroundColor: "#f43f5e",
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: { color: "#9ca3af" },
                    grid: { color: "rgba(255, 255, 255, 0.05)" }
                },
                y: {
                    ticks: { color: "#9ca3af", font: { size: 10 } },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderRecentTable(recentList) {
    const tbody = document.getElementById("recent-assessments-body");
    if (!recentList || recentList.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">No assessments recorded yet.</td></tr>`;
        return;
    }

    tbody.innerHTML = recentList.map(a => `
        <tr>
            <td style="font-family: var(--font-mono); font-weight: 600; color: var(--accent-cyan);">${a.assessment_id}</td>
            <td style="color: var(--text-muted); font-size: 0.85rem;">${a.created_at}</td>
            <td>
                <strong>${a.overall_score}</strong> / 100
            </td>
            <td>${getRiskBadge(a.risk_level)}</td>
            <td>
                <div style="display: flex; gap: 0.5rem;">
                    <a href="/report.html?id=${a.assessment_id}" class="btn btn-secondary" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;">
                        <i class="fa-solid fa-file-lines"></i> Report
                    </a>
                    <a href="/simulator.html?id=${a.assessment_id}" class="btn btn-secondary" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;">
                        <i class="fa-solid fa-sliders"></i> Simulate
                    </a>
                    <button onclick="handleDelete('${a.assessment_id}')" class="btn btn-danger" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join("");
}

window.handleDelete = async function(assessmentId) {
    if (!confirm(`Permanently delete assessment ${assessmentId}? This action enforces GDPR Right to Erasure.`)) {
        return;
    }
    try {
        await apiRequest(`/assessment/${assessmentId}`, { method: "DELETE" });
        showToast(`Assessment ${assessmentId} deleted successfully.`, "info");
        await loadDashboardData();
    } catch (err) {
        showToast("Delete failed: " + err.message, "danger");
    }
};
