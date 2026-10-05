"""
Social Media Privacy Risk Assessment Framework
REST API Routes & Controller Layer

Provides defensive, privacy-preserving endpoints for the assessment workflow,
simulation engine, analytics dashboard, and local metadata sanitization.
"""

from flask import Blueprint, request, jsonify, send_file
import io

from backend.services.questionnaire_data import QUESTIONS, CATEGORIES
from backend.services.assessment_engine import run_assessment
from backend.services.improvement_simulator import simulate_privacy_improvement, SIMULATION_PRESETS
from backend.models.database import (
    save_assessment,
    get_assessment,
    delete_assessment,
    get_dashboard_stats,
    update_assessment_simulation
)
from backend.utils.metadata_inspector import extract_exif_metadata, strip_exif_metadata

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health status endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Social Media Privacy Risk Assessment API",
        "version": "1.0.0"
    }), 200


@api_bp.route("/questionnaire", methods=["GET"])
def get_questionnaire():
    """Returns questionnaire categories, metadata, and all 44 assessment questions."""
    return jsonify({
        "categories": CATEGORIES,
        "questions": QUESTIONS,
        "total_questions": len(QUESTIONS)
    }), 200


@api_bp.route("/assessment", methods=["POST"])
def submit_assessment():
    """
    Submits questionnaire responses, calculates privacy risk score,
    generates findings & recommendations, and safely persists telemetry.
    """
    data = request.get_json() or {}
    responses = data.get("responses", {})
    custom_weights = data.get("custom_weights", None)

    if not isinstance(responses, dict):
        return jsonify({"error": "Invalid format: 'responses' must be an object."}), 400

    # Execute risk assessment pipeline
    result = run_assessment(responses, custom_weights)

    # Persist in privacy-first database
    try:
        save_assessment(result)
    except Exception as e:
        # Continue even if DB persistence fails in transient environments
        print(f"Database save notice: {e}")

    return jsonify(result), 201


@api_bp.route("/assessment/<assessment_id>", methods=["GET"])
def retrieve_assessment(assessment_id: str):
    """Retrieves an existing assessment by its anonymized ID."""
    assessment = get_assessment(assessment_id)
    if not assessment:
        return jsonify({"error": "Assessment not found."}), 404
    return jsonify(assessment), 200


@api_bp.route("/assessment/<assessment_id>/recommendations", methods=["GET"])
def retrieve_recommendations(assessment_id: str):
    """Retrieves prioritized recommendations for a specific assessment."""
    assessment = get_assessment(assessment_id)
    if not assessment:
        return jsonify({"error": "Assessment not found."}), 404
    return jsonify({
        "assessment_id": assessment_id,
        "recommendations": assessment.get("recommendations", [])
    }), 200


@api_bp.route("/assessment/simulate-improvement", methods=["POST"])
def simulate_improvement():
    """
    Simulates hypothetical privacy improvements on user responses.
    Accepts either an assessment_id or raw responses plus a list of selected improvement keys.
    """
    data = request.get_json() or {}
    assessment_id = data.get("assessment_id")
    selected_improvements = data.get("improvements", [])
    responses = data.get("responses")

    if assessment_id and not responses:
        assessment = get_assessment(assessment_id)
        if assessment:
            responses = assessment.get("cleaned_responses", {})
        else:
            return jsonify({"error": "Assessment ID not found."}), 404

    if not responses:
        return jsonify({"error": "No assessment responses available for simulation."}), 400

    simulation_result = simulate_privacy_improvement(responses, selected_improvements)

    # If linked to an assessment ID, update record
    if assessment_id:
        try:
            update_assessment_simulation(
                assessment_id,
                simulation_result["simulated"]["overall_score"],
                simulation_result["points_reduced"]
            )
        except Exception:
            pass

    return jsonify(simulation_result), 200


@api_bp.route("/assessment/<assessment_id>", methods=["DELETE"])
def remove_assessment(assessment_id: str):
    """Enforces Right to Erasure / GDPR data deletion."""
    deleted = delete_assessment(assessment_id)
    if deleted:
        return jsonify({"message": f"Assessment {assessment_id} and all related records deleted."}), 200
    return jsonify({"error": "Assessment not found or already deleted."}), 404


@api_bp.route("/dashboard/stats", methods=["GET"])
def dashboard_stats():
    """Returns privacy-safe aggregated dashboard statistics."""
    try:
        stats = get_dashboard_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"Failed to load dashboard metrics: {str(e)}"}), 500


@api_bp.route("/privacy-checklist", methods=["GET"])
def get_privacy_checklist():
    """Returns downloadable/printable defensive social media privacy checklist."""
    checklist = [
        {"item": "Review and tighten profile visibility (Friends-Only or Private)", "category": "Profile Visibility"},
        {"item": "Hide phone number and personal email address from public bio", "category": "Personal Information"},
        {"item": "Remove full birth year from public display", "category": "Personal Information"},
        {"item": "Disable real-time live location broadcasts and story geotags", "category": "Location Privacy"},
        {"item": "Adopt delayed venue check-ins (post after departing location)", "category": "Location Privacy"},
        {"item": "Avoid announcing upcoming vacation dates before or during travel", "category": "Location Privacy"},
        {"item": "Enable Tag Review so tagged photos require approval before appearing on profile", "category": "Tagging & Mentions"},
        {"item": "Restrict who can tag and @mention your profile", "category": "Tagging & Mentions"},
        {"item": "Verify unfamiliar connection or friend requests out-of-band before accepting", "category": "Friends & Followers"},
        {"item": "Conduct a biannual audit of followers and friends list", "category": "Friends & Followers"},
        {"item": "Enable Multi-Factor Authentication (MFA) via Authenticator App (TOTP)", "category": "Authentication"},
        {"item": "Generate unique 16+ character passwords stored in a password manager", "category": "Authentication"},
        {"item": "Turn on alerts for unrecognized logins from new devices/browsers", "category": "Authentication"},
        {"item": "Review and terminate stale active sessions across old devices", "category": "Authentication"},
        {"item": "Audit connected third-party OAuth apps and revoke dormant integrations", "category": "Third-Party Apps"},
        {"item": "Revoke excessive permissions (contacts, messages) granted to external apps", "category": "Third-Party Apps"},
        {"item": "Never click unsolicited DM links claiming 'Is this you in this video?'", "category": "Social Engineering"},
        {"item": "Never share SMS or 2FA verification codes with anyone under any pretext", "category": "Social Engineering"},
        {"item": "Audit and mass-privatize historical public posts from 3+ years ago", "category": "Digital Footprint"},
        {"item": "Delete or secure abandoned legacy accounts on older social networks", "category": "Digital Footprint"}
    ]
    return jsonify({"checklist": checklist, "total_items": len(checklist)}), 200


@api_bp.route("/metadata/inspect", methods=["POST"])
def inspect_image_metadata():
    """
    Inspects image EXIF metadata locally.
    Does NOT store the image on disk or transmit it externally.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    file = request.files["image"]
    image_bytes = file.read()

    metadata = extract_exif_metadata(image_bytes)
    return jsonify(metadata), 200


@api_bp.route("/metadata/sanitize", methods=["POST"])
def sanitize_image():
    """
    Strips all EXIF metadata from the provided image and returns a clean image download.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    file = request.files["image"]
    image_bytes = file.read()

    clean_bytes = strip_exif_metadata(image_bytes)
    return send_file(
        io.BytesIO(clean_bytes),
        mimetype="image/jpeg",
        as_attachment=True,
        download_name=f"sanitized_{file.filename or 'photo.jpg'}"
    )
