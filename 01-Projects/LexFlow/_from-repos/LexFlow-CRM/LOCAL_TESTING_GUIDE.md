# LexFlow CRM - LOCAL TESTING GUIDE

## Setup
```bash
cd ~/Desktop/LexFlow/lexflow_hermes_v1
source local_venv/bin/activate
pip install -r requirements.txt
```

## Start the Application

### Terminal 1: Run the CRM app
```bash
cd ~/Desktop/LexFlow/lexflow_hermes_v1
source local_venv/bin/activate
python run_crm.py
```

The app will start at `http://localhost:5001`

### Terminal 2: Run tests
Use the same virtual environment.

---

## Test Suite (30+ Checks)

### PHASE 1: Health & Basic Connectivity

**T1.1** Health check endpoint
```bash
curl -X GET http://localhost:5001/health
# Expected: 200 OK with {"status": "operational"}
```

**T1.2** Admin health endpoint (no auth required)
```bash
curl -X GET http://localhost:5001/api/admin/health
# Expected: 200 OK with {"status": "Admin endpoint operational"}
```

**T1.3** Invalid endpoint returns 404
```bash
curl -X GET http://localhost:5001/api/invalid
# Expected: 404 with {"error": "Not found"}
```

---

### PHASE 2: JWT & Authentication

**T2.1** Login with valid credentials
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@lexflow.com", "password": "SecurePass123"}'
# Expected: 200 OK with access_token
# Save token as: TOKEN=<access_token_value>
```

**T2.2** Login with invalid email format
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid-email", "password": "SecurePass123"}'
# Expected: 400 Bad Request with "Invalid email format"
```

**T2.3** Login with missing password
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@lexflow.com"}'
# Expected: 400 Bad Request
```

**T2.4** Login with wrong password
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@lexflow.com", "password": "WrongPassword123"}'
# Expected: 401 Unauthorized
```

**T2.5** Get current user with valid token
```bash
curl -X GET http://localhost:5001/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
# Expected: 200 OK with user data
```

**T2.6** Get current user without token
```bash
curl -X GET http://localhost:5001/api/auth/me
# Expected: 401 Unauthorized (missing token)
```

**T2.7** Get current user with invalid token
```bash
curl -X GET http://localhost:5001/api/auth/me \
  -H "Authorization: Bearer invalid-token"
# Expected: 422 Unprocessable Entity (invalid token)
```

**T2.8** Rate limiting on login (10 per minute)
```bash
# Send 11 rapid login attempts
for i in {1..11}; do
  curl -s -X POST http://localhost:5001/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email": "admin@lexflow.com", "password": "wrong"}'
done
# Expected: 11th request returns 429 Too Many Requests
```

---

### PHASE 3: Input Validation

**T3.1** Create case with valid data
```bash
curl -X POST http://localhost:5001/api/cases \
  -H "Content-Type: application/json" \
  -d '{
    "contactid": 1,
    "title": "Test Case Title",
    "status": "Intake",
    "priority": "Medium"
  }'
# Expected: 201 Created with case data
```

**T3.2** Create case with short title (should fail - min 3 chars)
```bash
curl -X POST http://localhost:5001/api/cases \
  -H "Content-Type: application/json" \
  -d '{"contactid": 1, "title": "AB", "status": "Intake"}'
# Expected: 400 Bad Request with "title must be at least 3 characters"
```

**T3.3** Create case with invalid status
```bash
curl -X POST http://localhost:5001/api/cases \
  -H "Content-Type: application/json" \
  -d '{
    "contactid": 1,
    "title": "Test Case",
    "status": "InvalidStatus"
  }'
# Expected: 400 Bad Request with "status must be one of: Intake, Active, Closed, On Hold"
```

**T3.4** Create case with invalid priority
```bash
curl -X POST http://localhost:5001/api/cases \
  -H "Content-Type: application/json" \
  -d '{
    "contactid": 1,
    "title": "Test Case",
    "priority": "VeryHigh"
  }'
# Expected: 400 Bad Request with "priority must be one of: Low, Medium, High, Critical"
```

**T3.5** Create case with invalid date format
```bash
curl -X POST http://localhost:5001/api/cases \
  -H "Content-Type: application/json" \
  -d '{
    "contactid": 1,
    "title": "Test Case",
    "openedat": "2026/01/01"
  }'
# Expected: 400 Bad Request with "openedat must be in ISO format (YYYY-MM-DD)"
```

**T3.6** Create case with non-integer contactid
```bash
curl -X POST http://localhost:5001/api/cases \
  -H "Content-Type: application/json" \
  -d '{"contactid": "invalid", "title": "Test Case"}'
# Expected: 400 Bad Request with "contactid must be an integer"
```

**T3.7** Create case with missing required field
```bash
curl -X POST http://localhost:5001/api/cases \
  -H "Content-Type: application/json" \
  -d '{"contactid": 1}'
# Expected: 400 Bad Request with "title is required"
```

---

### PHASE 4: Rate Limiting

**T4.1** Get cases within rate limit
```bash
for i in {1..50}; do
  curl -s http://localhost:5001/api/cases > /dev/null
done
# Expected: All requests succeed (60/minute limit)
```

**T4.2** Exceed read rate limit (60/minute for GET /cases)
```bash
for i in {1..65}; do
  curl -s http://localhost:5001/api/cases > /dev/null &
done
wait
# Expected: Some requests return 429 Too Many Requests
```

**T4.3** Create task rate limiting (30/minute for POST)
```bash
# Make 35 POST requests rapidly
for i in {1..35}; do
  curl -s -X POST http://localhost:5001/api/tasks \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"caseid": 1, "title": "Task '$i'"}' > /dev/null &
done
wait
# Expected: Some requests return 429 Too Many Requests
```

---

### PHASE 5: Admin Endpoints

**T5.1** List all users (requires admin role)
```bash
curl -X GET http://localhost:5001/api/admin/users \
  -H "Authorization: Bearer $TOKEN"
# Expected: 200 OK or 403 Forbidden (depending on user role)
```

**T5.2** Attempt to access admin endpoint without auth
```bash
curl -X GET http://localhost:5001/api/admin/users
# Expected: 401 Unauthorized
```

**T5.3** Get admin stats
```bash
curl -X GET http://localhost:5001/api/admin/stats \
  -H "Authorization: Bearer $TOKEN"
# Expected: 200 OK with stats or 403 Forbidden
```

---

### PHASE 6: CORS Configuration

**T6.1** Preflight CORS request
```bash
curl -X OPTIONS http://localhost:5001/api/cases \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET"
# Expected: 200 OK with CORS headers
```

**T6.2** Check CORS headers in response
```bash
curl -i -X GET http://localhost:5001/api/cases \
  -H "Origin: http://localhost:3000" | grep -i access-control
# Expected: Access-Control-Allow-Origin: http://localhost:3000
```

---

### PHASE 7: Connection Pooling

**T7.1** Concurrent connections (verify no connection errors)
```bash
# Make 50 concurrent requests
for i in {1..50}; do
  curl -s http://localhost:5001/api/cases > /dev/null &
done
wait
# Expected: All requests succeed without connection pool errors
```

**T7.2** Check database connection pooling (logs should show pool reuse)
```bash
# Watch Flask logs for "pool_pre_ping" operations
# Should see efficient connection reuse, not new connections for each request
```

---

### PHASE 8: Token Expiry

**T8.1** Verify JWT token expiry is set (should be 24 hours)
```bash
# On startup, app should show:
# JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
python -c "from crm import create_app; app = create_app(); print(app.config['JWT_ACCESS_TOKEN_EXPIRES'])"
# Expected: 1 day, 0:00:00
```

**T8.2** Manually test token expiry (after 24 hours)
```bash
# This requires waiting 24 hours or modifying JWT_EXPIRATION_HOURS env var
export JWT_EXPIRATION_HOURS=0.00007  # ~0.3 seconds
# Restart app
python run_crm.py
# Login, wait 1 second, try to use token
# Expected: Token becomes invalid after expiry time
```

---

### PHASE 9: Soft Delete Verification

**T9.1** Verify soft-deleted cases are hidden
```bash
# Create and delete a case, verify it doesn't appear in list
curl -X POST http://localhost:5001/api/cases \
  -H "Content-Type: application/json" \
  -d '{"contactid": 1, "title": "Delete Me", "status": "Intake"}' | jq '.id'
# Save as: CASE_ID=<id>

curl -X DELETE "http://localhost:5001/api/cases/$CASE_ID"
# Expected: 200 OK with {"deleted": true}

curl -X GET http://localhost:5001/api/cases | jq '.[] | select(.id == '$CASE_ID')'
# Expected: Empty result (soft-deleted case hidden)
```

**T9.2** Direct retrieval of soft-deleted case returns 404
```bash
curl -X GET "http://localhost:5001/api/cases/$CASE_ID"
# Expected: 404 Not Found (soft-deleted, filtered out)
```

---

### PHASE 10: Request/Response Format

**T10.1** All responses are valid JSON
```bash
curl -s http://localhost:5001/api/cases | jq . > /dev/null
# Expected: Exit code 0 (valid JSON)
```

**T10.2** Error responses have error field
```bash
curl -s -X POST http://localhost:5001/api/cases \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.error'
# Expected: Non-null error message
```

**T10.3** Success responses have correct status codes
```bash
# GET should return 200
curl -i -s http://localhost:5001/api/cases | head -1
# Expected: HTTP/1.1 200 OK

# POST should return 201 (or appropriate status)
curl -i -s http://localhost:5001/api/cases \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"contactid": 1, "title": "Test"}' | head -1
# Expected: HTTP/1.1 201 CREATED
```

---

## Database Verification

**DB1** Check migrations applied
```bash
cd ~/Desktop/LexFlow/lexflow_hermes_v1
source local_venv/bin/activate
flask db current
# Expected: Should show latest migration version
```

**DB2** Verify soft-delete columns exist
```bash
sqlite3 crm_local.db ".schema cases" | grep is_deleted
# Expected: Output shows is_deleted and deleted_at columns
```

---

## Performance Checks

**P1** Response time for GET /cases (should be <100ms)
```bash
curl -w "Time: %{time_total}s\n" -o /dev/null -s http://localhost:5001/api/cases
# Expected: Time under 0.1s (100ms)
```

**P2** Response time for authenticated request (should be <100ms)
```bash
curl -w "Time: %{time_total}s\n" -o /dev/null -s \
  -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/tasks
# Expected: Time under 0.1s (100ms)
```

---

## Cleanup

```bash
# Stop the Flask app (Ctrl+C in Terminal 1)
# Clean up test data
rm crm_local.db  # Recreate fresh DB if needed
```

---

## Test Summary Template

Copy this template and fill out after running tests:

```
LEXFLOW LOCAL TESTING RESULTS
==============================

Date: [DATE]
Tester: [NAME]
Build: lexflow_hermes_v1

PHASE 1 - Health & Connectivity:     [PASS/FAIL] [Details]
PHASE 2 - JWT & Authentication:      [PASS/FAIL] [Details]
PHASE 3 - Input Validation:          [PASS/FAIL] [Details]
PHASE 4 - Rate Limiting:             [PASS/FAIL] [Details]
PHASE 5 - Admin Endpoints:           [PASS/FAIL] [Details]
PHASE 6 - CORS Configuration:        [PASS/FAIL] [Details]
PHASE 7 - Connection Pooling:        [PASS/FAIL] [Details]
PHASE 8 - Token Expiry:              [PASS/FAIL] [Details]
PHASE 9 - Soft Delete Verification:  [PASS/FAIL] [Details]
PHASE 10 - Request/Response Format:  [PASS/FAIL] [Details]

Database Verification:               [PASS/FAIL] [Details]
Performance Checks:                  [PASS/FAIL] [Details]

OVERALL RESULT: [PASS/FAIL]

Issues Found:
- [List any issues]

Recommendations:
- [List recommendations]
```

---

## Troubleshooting

### App won't start
```bash
# Check Python version (should be 3.9+)
python --version

# Check dependencies
pip list | grep -E "Flask|SQLAlchemy|flask-cors|Flask-JWT|Flask-Limiter"

# Check for port conflicts
lsof -i :5001
```

### Database errors
```bash
# Reset database
rm crm_local.db
flask db upgrade
```

### JWT issues
```bash
# Check JWT secret is set
echo $JWT_SECRET_KEY

# Or set temporarily
export JWT_SECRET_KEY="test-secret-key"
```

### CORS errors in frontend
```bash
# Check CORS origins are configured
export CORS_ORIGINS="http://localhost:3000,http://localhost:5000,http://localhost:5001"
```

---

## Important Notes

1. **Rate Limiting**: Uses in-memory storage for local development. Production should use Redis.
2. **JWT Expiry**: Set to 24 hours. Change with `JWT_EXPIRATION_HOURS` env var.
3. **Connection Pooling**: Configured with 10 connections, 20 overflow. Tune for production load.
4. **Admin Access**: Requires user with `role='admin'` in database.
5. **Soft Deletes**: All deleted records are filtered server-side; recovery possible from DB.

