from flask import Flask, jsonify
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate, jwt
from .utils import setup_logging, log_request, log_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Setup CORS
    cors_origins = getattr(Config, 'CORS_ORIGINS', ["http://localhost:3000"])
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})
    
    # Setup logging
    setup_logging()
    
    # Setup rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Register request/response logging middleware
    @app.before_request
    def before_request():
        log_request()
    
    @app.after_request
    def after_request(response):
        return log_response(response)

    # Import models for migrations
    from .models.contact import Contact
    from .models.case import Case
    from .models.case_participant import CaseParticipant
    from .models.task import Task
    from .models.user import User
    from .models.deadline import Deadline
    from .models.event import Event

    # Register blueprints
    from .routes.health import health_bp
    from .routes.contacts import contacts_bp
    from .routes.cases import cases_bp
    from .routes.auth import auth_bp
    from .routes.tasks import tasks_bp
    from .routes.deadlines import deadlines_bp
    from .routes.events import events_bp
    from .routes.webhooks import webhooks_bp
    from .routes.admin import admin_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(cases_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(deadlines_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(webhooks_bp)
    app.register_blueprint(admin_bp)

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad request",
            "code": "BAD_REQUEST",
            "field": None
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not found",
            "code": "NOT_FOUND",
            "field": None
        }), 404

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            "error": "Conflict",
            "code": "CONFLICT",
            "field": None
        }), 409

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            "error": "Rate limit exceeded",
            "code": "RATE_LIMIT_EXCEEDED",
            "field": None
        }), 429

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "error": "Internal server error",
            "code": "SERVER_ERROR",
            "field": None
        }), 500

    return app
