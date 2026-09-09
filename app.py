import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from services.seed_data import seed_database
from routes.auth_routes import auth_bp
from routes.events_routes import events_bp
from routes.registrations_routes import registrations_bp
from routes.notifications_routes import notifications_bp
from routes.analytics_routes import analytics_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for all frontend origins
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(registrations_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(analytics_bp)

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "healthy",
            "app": "CampusEvents REST API",
            "version": "1.0.0"
        }), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": "Endpoint not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"success": False, "error": "Internal server error occurred"}), 500

    # Auto seed initial database documents
    try:
        seed_database()
    except Exception as e:
        print(f"[CampusEvents] Seeding notice: {e}")

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f" * CampusEvents Backend running on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
