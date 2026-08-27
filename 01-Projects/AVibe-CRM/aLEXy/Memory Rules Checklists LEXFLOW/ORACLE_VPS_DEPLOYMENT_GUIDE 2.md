# LexFlow Phase 1+2 — Oracle VPS Deployment Guide

**Project:** LexFlow CRM  
**Target:** Oracle Cloud Always Free VPS (Italy, EU residency)  
**Timeline:** 30-45 minutes  
**Status:** 🟡 READY TO EXECUTE — Awaiting Oracle VPS Credentials  

---

## 📋 PRE-DEPLOYMENT REQUIREMENTS

Before starting deployment, you must provide:

### 1. **Oracle VPS Instance Details**
- [ ] Public IP address (e.g., `152.67.100.123`)
- [ ] SSH username (typically `ubuntu` for Oracle Ubuntu images)
- [ ] SSH private key file path (e.g., `~/.ssh/oracle_lexflow_key`)

### 2. **Domain / DNS (Optional for SSL)**
- [ ] Domain name (e.g., `lexflow.io`) — can be added later
- [ ] Email for Let's Encrypt certificate renewal

### 3. **Database Credentials**
- Will be auto-generated during deployment
- Stored in `.env` on production server

### 4. **Project State**
- [x] LexFlow Phase 3g complete (last commit: 0dd36bc)
- [x] All dependencies in requirements.txt
- [x] Migrations prepared
- [x] Flask factory pattern ready (crm:create_app())

---

## 🚀 DEPLOYMENT PHASES

### Phase 0: Validation
**Duration:** ~2 minutes  
**Actions:**
- Verify SSH credentials provided
- Test SSH connectivity to Oracle VPS
- Confirm Python 3, PostgreSQL, nginx availability

**Commands:**
```bash
export ORACLE_VPS_IP="your-oracle-ip-here"
export ORACLE_SSH_USER="ubuntu"
export ORACLE_SSH_KEY_PATH="~/.ssh/oracle_lexflow_key"
export ORACLE_DOMAIN="your-domain.com"  # Optional

# Test SSH connection
ssh -i $ORACLE_SSH_KEY_PATH $ORACLE_SSH_USER@$ORACLE_VPS_IP "echo 'Connection successful'"
```

### Phase 1: System Update & Dependencies
**Duration:** ~5 minutes  
**What happens:**
- Updates apt packages
- Installs: Python3, PostgreSQL, nginx, git, certbot
- Installs: build tools for compiling dependencies

**Expected output:**
```
✅ System update and dependencies installed
```

### Phase 2: Clone Repository & Python Environment
**Duration:** ~3 minutes  
**What happens:**
- Clones LexFlow from GitHub to `/home/ubuntu/lexflow`
- Creates Python virtual environment
- Installs all Python dependencies (Flask, SQLAlchemy, Gunicorn, etc.)

**Expected output:**
```
✅ Repository cloned and Python environment ready
```

### Phase 3: PostgreSQL Database Setup
**Duration:** ~2 minutes  
**What happens:**
- Creates PostgreSQL database `lexflow_prod`
- Creates database user `lexflow_app` with strong password
- Grants necessary permissions

**IMPORTANT:** Save the database connection string:
```
postgresql://lexflow_app:[PASSWORD]@localhost:5432/lexflow_prod
```

**Expected output:**
```
✅ Database created: lexflow_prod
✅ Database user created: lexflow_app
⚠️  SAVE THIS: DATABASE_URL=postgresql://lexflow_app:***@localhost:5432/lexflow_prod
```

### Phase 4: Environment Configuration
**Duration:** ~1 minute  
**What happens:**
- Creates `.env` file with production configuration
- Sets Flask environment variables
- Generates JWT secrets

**Action needed:**
Update `.env` file on server with:
- DATABASE_URL (from Phase 3)
- Any third-party API keys (Resend, etc.)

```bash
ssh -i $ORACLE_SSH_KEY_PATH $ORACLE_SSH_USER@$ORACLE_VPS_IP "nano /home/ubuntu/lexflow/.env"
```

### Phase 5: Database Migrations
**Duration:** ~2 minutes  
**What happens:**
- Runs Flask-Migrate (alembic) to create all tables
- Sets up schema: users, contacts, cases, tasks, deadlines, etc.
- Applies soft-delete patterns

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade ...
✅ Database migrations completed
```

### Phase 6: Nginx Reverse Proxy
**Duration:** ~2 minutes  
**What happens:**
- Configures nginx as reverse proxy
- Routes HTTP/HTTPS traffic to gunicorn (localhost:8000)
- Enables compression, timeouts, client upload limit

**Configuration location:** `/etc/nginx/sites-available/lexflow-crm`

### Phase 7: Gunicorn Application Server
**Duration:** ~2 minutes  
**What happens:**
- Configures gunicorn worker pool (4 workers)
- Sets up supervisor systemd service
- Auto-starts on server reboot

**Service name:** `lexflow-gunicorn`  
**Logs:** `/home/ubuntu/lexflow/gunicorn.log`

### Phase 8: SSL/TLS Certificate (Let's Encrypt)
**Duration:** ~3-5 minutes (if domain provided)  
**What happens:**
- Requests SSL certificate via Let's Encrypt
- Configures auto-renewal (runs daily)
- Updates nginx to redirect HTTP → HTTPS

**Required:** Must provide domain name

**Expected output:**
```
✅ SSL certificate installed and auto-renewal configured
```

### Phase 9: Firewall Configuration
**Duration:** ~1 minute  
**What happens:**
- Enables UFW firewall
- Allows SSH (22), HTTP (80), HTTPS (443)
- Denies all other inbound traffic

**Expected output:**
```
🔥 Firewall status:
Status: active
To: 22/tcp ALLOW
To: 80/tcp ALLOW
To: 443/tcp ALLOW
```

### Phase 10: Health Check
**Duration:** ~1 minute  
**What happens:**
- Tests gunicorn responsiveness
- Checks supervisor service status
- Verifies nginx configuration
- Confirms database connectivity

**Test commands:**
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/auth/login

# Check service status
sudo supervisorctl status lexflow-gunicorn
sudo systemctl status nginx
sudo systemctl status postgresql
```

### Phase 11: Final Status Report
**Duration:** ~1 minute  
**Outputs:**
- Service status (gunicorn, nginx, PostgreSQL)
- Network configuration (IP address)
- Log locations for monitoring
- Summary of live URL

---

## 📊 EXECUTION

### Option A: Automated Deployment (Recommended)

```bash
# 1. Set your credentials
export ORACLE_VPS_IP="152.67.100.123"
export ORACLE_SSH_USER="ubuntu"
export ORACLE_SSH_KEY_PATH="~/.ssh/oracle_lexflow_key"
export ORACLE_DOMAIN="lexflow.io"  # Optional

# 2. Run deployment script
cd ~/Desktop/LexFlow/"LexFlow Review Build"
bash ORACLE_VPS_DEPLOYMENT_SCRIPT.sh

# 3. Follow on-screen prompts and save credentials
```

**Total time:** ~30-45 minutes (includes safeguards and monitoring)

### Option B: Manual Deployment (Step-by-Step)

If you prefer manual control, follow each phase section above with direct SSH commands.

---

## 🔧 POST-DEPLOYMENT TASKS

### 1. Update Database Connection String
```bash
ssh -i ~/.ssh/oracle_lexflow_key ubuntu@YOUR_IP
cd /home/ubuntu/lexflow
nano .env

# Add the DATABASE_URL from Phase 3
# Save and restart gunicorn
```

### 2. Configure Domain DNS (if using SSL)
Point your domain's A record to: `YOUR_ORACLE_VPS_IP`

### 3. Test Endpoints
```bash
# Health check
curl https://YOUR_DOMAIN/health

# API endpoints
curl -X POST https://YOUR_DOMAIN/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test"}'

curl https://YOUR_DOMAIN/api/contacts
```

### 4. Verify Database
```bash
ssh -i ~/.ssh/oracle_lexflow_key ubuntu@YOUR_IP

# Connect to PostgreSQL
psql -U lexflow_app -d lexflow_prod -h localhost

# Check tables
\dt

# Exit
\q
```

### 5. Check Logs
```bash
# Gunicorn logs
ssh ubuntu@YOUR_IP "tail -f /home/ubuntu/lexflow/gunicorn.log"

# Nginx logs
ssh ubuntu@YOUR_IP "sudo tail -f /var/log/nginx/access.log"

# PostgreSQL logs
ssh ubuntu@YOUR_IP "sudo tail -f /var/log/postgresql/postgresql.log"

# Supervisor logs
ssh ubuntu@YOUR_IP "sudo supervisorctl tail lexflow-gunicorn"
```

---

## ⚠️ TROUBLESHOOTING

### Issue: Connection refused (gunicorn not responding)
**Solution:**
```bash
ssh ubuntu@YOUR_IP
sudo supervisorctl status lexflow-gunicorn
sudo supervisorctl restart lexflow-gunicorn
tail -f /home/ubuntu/lexflow/gunicorn.log
```

### Issue: 502 Bad Gateway (nginx → gunicorn error)
**Check:**
- Gunicorn is running: `sudo supervisorctl status lexflow-gunicorn`
- Gunicorn can parse app: `flask shell` locally to test
- Database connection string in `.env` is correct
- Look at nginx error log: `sudo tail /var/log/nginx/error.log`

### Issue: Database connection failed
**Check:**
- PostgreSQL running: `sudo systemctl status postgresql`
- Database exists: `sudo -u postgres psql -l | grep lexflow_prod`
- User permissions: `sudo -u postgres psql -c "\du lexflow_app"`
- CONNECTION STRING format in `.env`

### Issue: SSL certificate not working
**Solution:**
```bash
# Check certificate status
sudo certbot certificates

# Force renewal
sudo certbot renew --force-renewal

# Check nginx config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

---

## 📈 MONITORING & MAINTENANCE

### Daily Checks
```bash
# Application health
curl https://YOUR_DOMAIN/health

# Check for errors in logs
ssh ubuntu@YOUR_IP "tail -n 50 /home/ubuntu/lexflow/gunicorn.log" | grep ERROR
```

### Weekly Tasks
```bash
# Check disk usage
ssh ubuntu@YOUR_IP "df -h"

# Check system load
ssh ubuntu@YOUR_IP "uptime"

# Backup database
ssh ubuntu@YOUR_IP "sudo -u postgres pg_dump lexflow_prod > /home/ubuntu/lexflow/backup/lexflow_prod_$(date +%Y%m%d).sql"
```

### Monthly Tasks
- Review PostgreSQL logs for slow queries
- Check for security updates: `sudo apt list --upgradable`
- Apply updates: `sudo apt-get update && sudo apt-get upgrade`
- Restart gunicorn after updates: `sudo supervisorctl restart lexflow-gunicorn`

---

## 🔐 SECURITY BEST PRACTICES

✅ **Already Configured:**
- SSH key-based authentication (no password)
- Firewall (UFW) restricting inbound traffic
- HTTPS/TLS encryption
- Strong database password (auto-generated)
- Gunicorn bind to localhost only (nginx proxy)

✅ **Recommended Additional:**
- Regular backups (set up cron job)
- Monitor failed login attempts
- Update system weekly: `sudo apt-get update && sudo apt-get upgrade`
- Regular security audits of code

---

## 📞 SUPPORT & ESCALATION

If deployment fails:

1. **Check connectivity:** `ssh -i KEY ubuntu@IP "echo ok"`
2. **Review script output:** Look for first ERROR
3. **Check logs:** Phase 10 provides log paths
4. **Re-run specific phase:** Can repeat individual phases
5. **Manual intervention:** SSH in and debug manually

**Rollback:** If deployment fails mid-way:
```bash
# SSH to VPS and check what was done
ssh -i $KEY ubuntu@$IP "ls -la /home/ubuntu/"

# You can safely re-run the deployment script
# It will detect existing components and continue
```

---

## ✅ SUCCESS CRITERIA

Deployment is successful when:

- [ ] SSH connection established to Oracle VPS
- [ ] apt packages updated
- [ ] Python 3 and PostgreSQL installed
- [ ] LexFlow repository cloned
- [ ] Python dependencies installed
- [ ] Database created and migrated
- [ ] Gunicorn service active
- [ ] Nginx proxying traffic
- [ ] SSL certificate installed (if domain provided)
- [ ] Firewall configured (22, 80, 443 open)
- [ ] Health endpoint responds: `/health`
- [ ] API endpoints accessible

---

## 📝 DEPLOYMENT RECORD

**Date Started:** [Will be filled during execution]  
**Date Completed:** [Will be filled during execution]  
**Deployed By:** Hermes Agent (Automated)  
**Project:** LexFlow CRM Phase 1+2  
**Target:** Oracle Cloud Always Free (Italy Region)  
**Live URL:** http://[ORACLE_VPS_IP] (or https://[DOMAIN] with SSL)  

---

**Next:** Provide Oracle VPS credentials and run `ORACLE_VPS_DEPLOYMENT_SCRIPT.sh`

## Links
- Parent: [[Memory Rules Checklists LEXFLOW-INDEX]]
- Related: [[ORACLE_VPS_CREDENTIALS_CHECKLIST 2]]
