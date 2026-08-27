#!/bin/bash
# Railway Environment Configuration for LexFlow Backend
# Run this script in Railway dashboard to set environment variables
# OR manually set them in Service Settings → Variables

# REQUIRED VARIABLES (Already in .env, but must be set on Railway):

export DATABASE_URL="postgresql://postgres:***@viaduct.proxy.rlwy.net:37017/railway"
# ^ Already configured from .env file

export FLASK_ENV="production"
# Sets Flask to production mode (no debug, no reloader)

export FLASK_APP="wsgi:app"
# Gunicorn knows to import from wsgi.py

export SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
# Generate a strong secret key for JWT signing

# OPTIONAL BUT RECOMMENDED:

export LOG_LEVEL="INFO"
# Sets logging verbosity

export GUNICORN_WORKERS="4"
# Number of Gunicorn worker processes

export GUNICORN_TIMEOUT="120"
# Worker process timeout (seconds)

# CHATBOT INTEGRATION (Phase 4):

export CHATBOT_URL="http://localhost:5000"
# Local development; change to public chatbot URL in production

# NETLIFY INTEGRATION:

export CORS_ORIGINS="https://poetic-kleicha-28d058.netlify.app,http://localhost:3000"
# Allow these origins to make API requests

# EMAIL NOTIFICATIONS (Already in .env):

export RESEND_API_KEY="re_YJA...LmW7"
# Resend email service API key

export EMAIL_FROM="onboarding@resend.dev"
export EMAIL_FROM_NAME="LexFlow"

# ADMIN FEATURES:

export ADMIN_EMAIL="olesya00007@yahoo.com"
# Email for admin notifications

export WEBHOOK_SECRET="34c9a0...fe76"
# Secret token for webhook verification

echo "✅ Environment variables configured for Railway"
echo ""
echo "To apply these in Railway:"
echo "1. Go to Railway dashboard"
echo "2. Select your LexFlow service"
echo "3. Go to Variables tab"
echo "4. Set each variable manually OR"
echo "5. Use Railway CLI: railway variable set KEY value"
