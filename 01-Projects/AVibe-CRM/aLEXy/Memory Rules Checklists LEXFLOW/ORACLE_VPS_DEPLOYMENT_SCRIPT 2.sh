#!/bin/bash

################################################################################
# LexFlow Phase 1+2 — Oracle VPS Deployment Script
# Target: Oracle Cloud Always Free (Ubuntu 20.04 LTS, Italy region EU residency)
# User: ubuntu (default Oracle image user)
# Timeline: 30-45 minutes
# Status: READY TO EXECUTE (awaiting credentials)
################################################################################

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration variables - UPDATE THESE WITH YOUR ORACLE VPS VALUES
ORACLE_VPS_IP="${ORACLE_VPS_IP:-}"                    # e.g., "152.67.100.123"
ORACLE_SSH_USER="${ORACLE_SSH_USER:-ubuntu}"           # Usually "ubuntu"
ORACLE_SSH_KEY_PATH="${ORACLE_SSH_KEY_PATH:-}"         # e.g., "~/.ssh/oracle_lexflow_key"
ORACLE_DOMAIN="${ORACLE_DOMAIN:-}"                     # e.g., "lexflow.io"
REPOSITORY_URL="https://github.com/olesiarasing/lexflow.git"  # Update if different
APP_NAME="lexflow-crm"
APP_DIR="/home/ubuntu/lexflow"
VENV_DIR="${APP_DIR}/.venv"

################################################################################
# PHASE 0: Validation & Pre-Deployment Checks
################################################################################

echo -e "${BLUE}=== PHASE 0: Validation & Pre-Deployment Checks ===${NC}"

# Check if credentials are provided
if [ -z "$ORACLE_VPS_IP" ]; then
    echo -e "${RED}❌ ERROR: ORACLE_VPS_IP not set${NC}"
    echo "Set it with: export ORACLE_VPS_IP='<your-oracle-vps-ip>'"
    exit 1
fi

if [ -z "$ORACLE_SSH_KEY_PATH" ]; then
    echo -e "${RED}❌ ERROR: ORACLE_SSH_KEY_PATH not set${NC}"
    echo "Set it with: export ORACLE_SSH_KEY_PATH='~/.ssh/oracle_lexflow_key'"
    exit 1
fi

# Expand tilde in path
ORACLE_SSH_KEY_PATH="${ORACLE_SSH_KEY_PATH/#\~/$HOME}"

if [ ! -f "$ORACLE_SSH_KEY_PATH" ]; then
    echo -e "${RED}❌ ERROR: SSH private key not found at $ORACLE_SSH_KEY_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Credentials validation passed${NC}"
echo "   Oracle VPS IP: $ORACLE_VPS_IP"
echo "   SSH User: $ORACLE_SSH_USER"
echo "   SSH Key: $ORACLE_SSH_KEY_PATH"
echo ""

################################################################################
# PHASE 1: Connect to Oracle VPS & System Update
################################################################################

echo -e "${BLUE}=== PHASE 1: System Update & Dependencies ===${NC}"

ssh -i "$ORACLE_SSH_KEY_PATH" "$ORACLE_SSH_USER@$ORACLE_VPS_IP" << 'EOF'
set -e
echo "🔄 Updating system packages..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

echo "📦 Installing dependencies..."
sudo apt-get install -y -qq \
    build-essential \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    nginx \
    git \
    curl \
    wget \
    certbot \
    python3-certbot-nginx \
    supervisor \
    ufw

echo -e "\033[0;32m✅ System update and dependencies installed\033[0m"
EOF

echo ""

################################################################################
# PHASE 2: Clone Project & Setup Python Environment
################################################################################

echo -e "${BLUE}=== PHASE 2: Clone Repository & Setup Python Environment ===${NC}"

ssh -i "$ORACLE_SSH_KEY_PATH" "$ORACLE_SSH_USER@$ORACLE_VPS_IP" << EOF
set -e

# Clone repository if not already present
if [ ! -d "$APP_DIR" ]; then
    echo "📚 Cloning LexFlow repository..."
    git clone $REPOSITORY_URL $APP_DIR
else
    echo "📚 Repository already exists, pulling latest changes..."
    cd $APP_DIR
    git pull origin main || git pull origin master
fi

cd $APP_DIR

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv $VENV_DIR

# Activate and upgrade pip
source $VENV_DIR/bin/activate
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo -e "\033[0;32m✅ Repository cloned and Python environment ready\033[0m"
EOF

echo ""

################################################################################
# PHASE 3: PostgreSQL Database Setup
################################################################################

echo -e "${BLUE}=== PHASE 3: PostgreSQL Database Setup ===${NC}"

ssh -i "$ORACLE_SSH_KEY_PATH" "$ORACLE_SSH_USER@$ORACLE_VPS_IP" << 'EOF'
set -e

# Generate strong database password
DB_PASSWORD=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
DB_NAME="lexflow_prod"
DB_USER="lexflow_app"

echo "🗄️  Creating PostgreSQL database and user..."

# Create database and user
sudo -u postgres psql << PSQL_EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET default_transaction_deferrable TO on;
ALTER ROLE $DB_USER SET default_transaction_level TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\c $DB_NAME
GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;
PSQL_EOF

echo "✅ Database created: $DB_NAME"
echo "✅ Database user created: $DB_USER"
echo "⚠️  SAVE THIS: DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME"

EOF

echo ""

################################################################################
# PHASE 4: Environment Configuration
################################################################################

echo -e "${BLUE}=== PHASE 4: Environment Configuration ===${NC}"

ssh -i "$ORACLE_SSH_KEY_PATH" "$ORACLE_SSH_USER@$ORACLE_VPS_IP" << 'EOF'
set -e

cd /home/ubuntu/lexflow

# Create .env file with production variables
cat > .env << 'ENVFILE'
# LexFlow Production Environment — Oracle VPS
FLASK_ENV=production
FLASK_APP=crm
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')

# PostgreSQL (set DATABASE_URL from Phase 3)
# DATABASE_URL=postgresql://lexflow_app:PASSWORD@localhost:5432/lexflow_prod

# API Configuration
SERVER_NAME=localhost
ALLOWED_HOSTS=["*"]

# JWT Configuration
JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
JWT_ALGORITHM=HS256

# Optional: Third-party integrations (populate if using)
RESEND_API_KEY=
EMAIL_FROM=noreply@lexflow.io
WEBHOOK_SECRET=

# Logging
LOG_LEVEL=INFO
ENVFILE

echo "✅ .env file created"
echo "⚠️  UPDATE .env with actual DATABASE_URL and other secrets!"

EOF

echo ""

################################################################################
# PHASE 5: Database Migrations
################################################################################

echo -e "${BLUE}=== PHASE 5: Database Migrations ===${NC}"

ssh -i "$ORACLE_SSH_KEY_PATH" "$ORACLE_SSH_USER@$ORACLE_VPS_IP" << EOF
set -e

cd $APP_DIR
source $VENV_DIR/bin/activate

echo "🔄 Running database migrations..."
FLASK_APP=crm flask db upgrade

echo -e "\033[0;32m✅ Database migrations completed\033[0m"
EOF

echo ""

################################################################################
# PHASE 6: Nginx Configuration
################################################################################

echo -e "${BLUE}=== PHASE 6: Nginx Configuration ===${NC}"

ssh -i "$ORACLE_SSH_KEY_PATH" "$ORACLE_SSH_USER@$ORACLE_VPS_IP" << EOF
set -e

# Create nginx config
sudo tee /etc/nginx/sites-available/$APP_NAME > /dev/null << 'NGINX'
upstream gunicorn {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    listen [::]:80;
    server_name _;  # Change to your domain

    client_max_body_size 10M;

    location / {
        proxy_pass http://gunicorn;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files (if needed)
    location /static/ {
        alias $APP_DIR/static/;
        expires 30d;
    }
}
NGINX

# Enable the site
sudo ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/$APP_NAME
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

echo -e "\033[0;32m✅ Nginx configured and reloaded\033[0m"
EOF

echo ""

################################################################################
# PHASE 7: Gunicorn & Supervisor Setup
################################################################################

echo -e "${BLUE}=== PHASE 7: Gunicorn & Supervisor Service Setup ===${NC}"

ssh -i "$ORACLE_SSH_KEY_PATH" "$ORACLE_SSH_USER@$ORACLE_VPS_IP" << EOF
set -e

# Create supervisor config for gunicorn
sudo tee /etc/supervisor/conf.d/$APP_NAME.conf > /dev/null << 'SUPERVISOR'
[program:lexflow-gunicorn]
directory=$APP_DIR
command=$VENV_DIR/bin/gunicorn --workers 4 --worker-class sync --bind 127.0.0.1:8000 --timeout 60 --access-logfile - --error-logfile - crm:create_app()
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$APP_DIR/gunicorn.log
environment=FLASK_ENV=production,PATH=$VENV_DIR/bin
SUPERVISOR

# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start lexflow-gunicorn

echo -e "\033[0;32m✅ Gunicorn service started via supervisor\033[0m"
EOF

echo ""

################################################################################
# PHASE 8: SSL/TLS with Let's Encrypt
################################################################################

echo -e "${BLUE}=== PHASE 8: SSL/TLS Setup (Let's Encrypt) ===${NC}"

if [ -z "$ORACLE_DOMAIN" ]; then
    echo -e "${YELLOW}⚠️  ORACLE_DOMAIN not set. Skipping SSL setup.${NC}"
    echo "   To enable SSL later, run:"
    echo "   sudo certbot --nginx -d $ORACLE_DOMAIN"
else
    ssh -i "$ORACLE_SSH_KEY_PATH" "$ORACLE_SSH_USER@$ORACLE_VPS_IP" << EOF
set -e

echo "🔐 Setting up SSL certificate with Let's Encrypt..."
sudo certbot --nginx -d $ORACLE_DOMAIN --non-interactive --agree-tos -m admin@$ORACLE_DOMAIN

echo -e "\033[0;32m✅ SSL certificate installed and auto-renewal configured\033[0m"
EOF
fi

echo ""

################################################################################
# PHASE 9: Firewall Setup (UFW)
################################################################################

echo -e "${BLUE}=== PHASE 9: Firewall Configuration ===${NC}"

ssh -i "$ORACLE_SSH_KEY_PATH" "$ORACLE_SSH_USER@$ORACLE_VPS_IP" << 'EOF'
set -e

echo "🔒 Configuring firewall..."

# Enable UFW
sudo ufw --force enable

# Default policy
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (port 22)
sudo ufw allow 22/tcp

# Allow HTTP (port 80)
sudo ufw allow 80/tcp

# Allow HTTPS (port 443)
sudo ufw allow 443/tcp

# Show firewall status
echo "🔥 Firewall status:"
sudo ufw status

echo -e "\033[0;32m✅ Firewall configured (SSH, HTTP, HTTPS allowed)\033[0m"
EOF

echo ""

################################################################################
# PHASE 10: Health Check & Endpoint Testing
################################################################################

echo -e "${BLUE}=== PHASE 10: Health Check & Endpoint Testing ===${NC}"

ssh -i "$ORACLE_SSH_KEY_PATH" "$ORACLE_SSH_USER@$ORACLE_VPS_IP" << 'EOF'
set -e

echo "🏥 Checking application health..."

# Wait for gunicorn to start
sleep 5

# Test health endpoint
echo "  Testing /health endpoint..."
curl -s http://localhost:8000/health || echo "  ⚠️  /health endpoint not responding"

# Check supervisor status
echo "📊 Supervisor service status:"
sudo supervisorctl status lexflow-gunicorn

# Show nginx status
echo "🌐 Nginx status:"
sudo systemctl status nginx --no-pager

echo -e "\033[0;32m✅ Health check completed\033[0m"
EOF

echo ""

################################################################################
# PHASE 11: Final Status Report
################################################################################

echo -e "${BLUE}=== PHASE 11: Deployment Status Report ===${NC}"

DEPLOYMENT_REPORT=$(ssh -i "$ORACLE_SSH_KEY_PATH" "$ORACLE_SSH_USER@$ORACLE_VPS_IP" << 'EOF'
echo "🚀 LEXFLOW V1 DEPLOYMENT - ORACLE VPS"
echo ""
echo "✅ Services Status:"
sudo supervisorctl status lexflow-gunicorn
sudo systemctl status nginx --no-pager | grep "Active"
echo ""
echo "📧 PostgreSQL:"
sudo systemctl status postgresql --no-pager | grep "Active"
echo ""
echo "🔒 Firewall:"
sudo ufw status | grep 'Status'
echo ""
echo "🌐 Network Configuration:"
hostname -I | awk '{print "   Primary IP: " $1}'
echo ""
echo "📝 Logs:"
echo "   Gunicorn: sudo tail -f /home/ubuntu/lexflow/gunicorn.log"
echo "   Nginx: sudo tail -f /var/log/nginx/access.log"
echo "   PostgreSQL: sudo tail -f /var/log/postgresql/postgresql.log"
echo ""
EOF
)

echo "$DEPLOYMENT_REPORT"

################################################################################
# Summary
################################################################################

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ DEPLOYMENT COMPLETED${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "🎯 Next Steps:"
echo "1. Update .env with DATABASE_URL and other secrets"
echo "2. Restart gunicorn: sudo supervisorctl restart lexflow-gunicorn"
echo "3. Point domain DNS to: $ORACLE_VPS_IP"
echo "4. Test endpoints:"
echo "   curl http://$ORACLE_VPS_IP/api/auth/login"
echo "   curl http://$ORACLE_VPS_IP/api/contacts"
echo "5. Monitor logs:"
echo "   ssh -i $ORACLE_SSH_KEY_PATH $ORACLE_SSH_USER@$ORACLE_VPS_IP 'sudo tail -f /home/ubuntu/lexflow/gunicorn.log'"
echo ""
echo "📊 Application accessible at: http://$ORACLE_VPS_IP"
echo ""
