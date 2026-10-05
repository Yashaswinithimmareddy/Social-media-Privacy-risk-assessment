/**
 * Social Media Privacy Risk Assessment Framework
 * Assessment Wizard Controller
 */

let questionnaireData = null;
let currentCategoryIndex = 0;
let userResponses = {};

const categoryKeys = ["CAT_A", "CAT_B", "CAT_C", "CAT_D", "CAT_E", "CAT_F", "CAT_G", "CAT_H", "CAT_I", "CAT_J"];

document.addEventListener("DOMContentLoaded", async () => {
    await loadQuestionnaire();
    setupEventListeners();
});

async function loadQuestionnaire() {
    try {
        questionnaireData = await apiRequest("/questionnaire");
        renderCategoryPills();
        renderCurrentCategory();
        updateProgress();
    } catch (err) {
        document.getElementById("questions-container").innerHTML = `
            <div class="callout callout-danger">
                <h4>Error loading questionnaire</h4>
                <p>${err.message}</p>
            </div>
        `;
    }
}

function renderCategoryPills() {
    const container = document.getElementById("category-pills-container");
    container.innerHTML = "";

    categoryKeys.forEach((catId, idx) => {
        const cat = questionnaireData.categories[catId];
        const pill = document.createElement("button");
        pill.type = "button";
        pill.className = `category-pill ${idx === currentCategoryIndex ? "active" : ""}`;
        pill.innerHTML = `<span>${idx + 1}. ${cat.name}</span>`;
        pill.addEventListener("click", () => {
            currentCategoryIndex = idx;
            renderCurrentCategory();
            updateProgress();
        });
        container.appendChild(pill);
    });
}

function renderCurrentCategory() {
    const catId = categoryKeys[currentCategoryIndex];
    const cat = questionnaireData.categories[catId];
    const catQuestions = questionnaireData.questions.filter(q => q.category === catId);

    const container = document.getElementById("questions-container");
    let html = `
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span class="badge badge-low" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4);">
                    Category ${currentCategoryIndex + 1} of 10
                </span>
                <span style="font-size: 0.85rem; color: var(--text-muted);">${Math.round(cat.weight * 100)}% Weight</span>
            </div>
            <h2 style="font-size: 1.5rem; font-weight: 700; margin-top: 0.35rem;">${cat.name}</h2>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">${cat.description}</p>
        </div>
    `;

    catQuestions.forEach((q, qIndex) => {
        const selectedVal = userResponses[q.id];
        html += `
            <div class="question-block" id="block-${q.id}">
                <div class="question-title">
                    <span style="color: var(--accent-cyan); font-family: var(--font-mono); margin-right: 0.5rem;">[${q.id.toUpperCase()}]</span>
                    ${q.question}
                </div>
                <div class="question-desc">
                    <i class="fa-solid fa-circle-info" style="color: var(--accent-blue);"></i> ${q.explanation}
                </div>
                <div class="options-group">
                    ${q.options.map(opt => `
                        <label class="option-label ${selectedVal === opt.value ? 'selected' : ''}">
                            <input type="radio" name="${q.id}" value="${opt.value}" 
                                   ${selectedVal === opt.value ? 'checked' : ''} 
                                   onchange="handleOptionSelect('${q.id}', '${opt.value}')">
                            <div>
                                <div style="font-weight: 500;">${opt.label}</div>
                            </div>
                        </label>
                    `).join("")}
                </div>
            </div>
        `;
    });

    container.innerHTML = html;

    // Update navigation buttons
    document.getElementById("btn-prev").disabled = (currentCategoryIndex === 0);
    const isLast = (currentCategoryIndex === categoryKeys.length - 1);
    document.getElementById("btn-next").style.display = isLast ? "none" : "inline-flex";
    document.getElementById("btn-submit").style.display = isLast ? "inline-flex" : "none";

    // Update active pill
    document.querySelectorAll(".category-pill").forEach((pill, idx) => {
        pill.classList.toggle("active", idx === currentCategoryIndex);
        const cid = categoryKeys[idx];
        const isCatDone = questionnaireData.questions.filter(q => q.category === cid).every(q => userResponses[q.id]);
        pill.classList.toggle("completed", isCatDone);
    });
}

window.handleOptionSelect = function(questionId, value) {
    userResponses[questionId] = value;
    const block = document.getElementById(`block-${questionId}`);
    if (block) {
        block.querySelectorAll(".option-label").forEach(lbl => {
            const input = lbl.querySelector("input");
            lbl.classList.toggle("selected", input.value === value);
        });
    }
    updateProgress();
};

function updateProgress() {
    if (!questionnaireData) return;
    const total = questionnaireData.questions.length;
    const answered = Object.keys(userResponses).length;
    const pct = Math.round((answered / total) * 100);

    const catId = categoryKeys[currentCategoryIndex];
    const cat = questionnaireData.categories[catId];

    document.getElementById("wizard-progress-category").textContent = `Category ${currentCategoryIndex + 1} of 10: ${cat.name}`;
    document.getElementById("wizard-progress-count").textContent = `${answered} of ${total} Questions Answered (${pct}%)`;
    document.getElementById("wizard-progress-bar").style.width = `${pct}%`;
}

function setupEventListeners() {
    document.getElementById("btn-prev").addEventListener("click", () => {
        if (currentCategoryIndex > 0) {
            currentCategoryIndex--;
            renderCurrentCategory();
            updateProgress();
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    });

    document.getElementById("btn-next").addEventListener("click", () => {
        if (currentCategoryIndex < categoryKeys.length - 1) {
            currentCategoryIndex++;
            renderCurrentCategory();
            updateProgress();
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    });

    document.getElementById("assessment-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const total = questionnaireData.questions.length;
        const answered = Object.keys(userResponses).length;

        if (answered < total) {
            if (!confirm(`You have answered ${answered} of ${total} questions. Unanswered questions will use moderate defaults. Proceed with risk calculation?`)) {
                return;
            }
        }

        const submitBtn = document.getElementById("btn-submit");
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Risk Vectors...`;

        try {
            const result = await apiRequest("/assessment", {
                method: "POST",
                body: JSON.stringify({ responses: userResponses })
            });

            // Store in session storage and redirect to report
            sessionStorage.setItem("last_assessment", JSON.stringify(result));
            window.location.href = `/report.html?id=${result.assessment_id}`;
        } catch (err) {
            alert(`Assessment error: ${err.message}`);
            submitBtn.disabled = false;
            submitBtn.innerHTML = `<i class="fa-solid fa-shield-virus"></i> Calculate Privacy Risk Score`;
        }
    });

    // Quick demo fills
    document.getElementById("btn-fill-safe").addEventListener("click", () => {
        quickFillDemo("safe");
    });

    document.getElementById("btn-fill-high").addEventListener("click", () => {
        quickFillDemo("high");
    });
}

function quickFillDemo(type) {
    if (!questionnaireData) return;
    questionnaireData.questions.forEach(q => {
        if (type === "safe") {
            // Pick lowest risk option
            const sorted = [...q.options].sort((a, b) => a.risk_score - b.risk_score);
            userResponses[q.id] = sorted[0].value;
        } else {
            // Pick highest risk option
            const sorted = [...q.options].sort((a, b) => b.risk_score - a.risk_score);
            userResponses[q.id] = sorted[0].value;
        }
    });
    renderCurrentCategory();
    updateProgress();
    showToast(
        type === "safe" 
            ? "Filled with Privacy-Conscious demo responses (Low Risk expected)."
            : "Filled with High-Exposure demo responses (Critical Risk expected).",
        type === "safe" ? "info" : "warning"
    );
}
