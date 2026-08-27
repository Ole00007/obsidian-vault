"""
WSGI entry point for Gunicorn/Railway deployment.
Imports the Flask app factory and creates the application instance.
"""
import os
from crm import create_app

# Create Flask app using factory pattern
app = create_app()

# Production-safe entry point
if __name__ == "__main__":
    # Local development only (Railway uses gunicorn wsgi:app)
    app.run(debug=False)
