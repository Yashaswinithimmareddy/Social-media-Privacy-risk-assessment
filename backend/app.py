"""
Social Media Privacy Risk Assessment Framework
Flask Main Application Entrypoint

Serves the REST API and the responsive cybersecurity frontend UI.
Implements defensive HTTP security headers and Privacy-by-Design controls.
"""

import os
import sys
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

# Add root folder to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.routes.api_routes import api_bp
from backend.models.database import init_db

def create_app() -> Flask:
    frontend_dir = os.path.join(root_dir, "frontend")
    app = Flask(__name__, static_folder=frontend_dir, static_url_path="")
    CORS(app)

    # Initialize SQLite database
    init_db()

    # Register API blueprint
    app.register_blueprint(api_bp)

    # Security Headers Middleware
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "img-src 'self' data: blob:; "
            "font-src 'self' https://cdnjs.cloudflare.com;"
        )
        return response

    # Frontend Route Handlers
    @app.route("/")
    def index():
        return send_from_directory(frontend_dir, "index.html")

    @app.route("/assessment")
    @app.route("/assessment.html")
    def assessment():
        return send_from_directory(frontend_dir, "assessment.html")

    @app.route("/dashboard")
    @app.route("/dashboard.html")
    def dashboard():
        return send_from_directory(frontend_dir, "dashboard.html")

    @app.route("/simulator")
    @app.route("/simulator.html")
    def simulator():
        return send_from_directory(frontend_dir, "simulator.html")

    @app.route("/metadata")
    @app.route("/metadata.html")
    def metadata_tool():
        return send_from_directory(frontend_dir, "metadata.html")

    @app.route("/report")
    @app.route("/report.html")
    def report_view():
        return send_from_directory(frontend_dir, "report.html")

    # Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Social Media Privacy Risk Assessment Framework running at http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=True)
