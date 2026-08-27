"""Admin endpoints for system diagnostics, status, and demo data."""
from flask import Blueprint, jsonify, request
from ..extensions import db
from ..clients.chatbot import ChatbotClient
from ..models.contact import Contact
from ..models.case import Case
from ..models.task import Task
from ..models.event import Event
from ..models.user import User
from ..models.deadline import Deadline
import logging
import os
from datetime import datetime, timedelta
from sqlalchemy import func

logger = logging.getLogger(__name__)
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("/status")
def admin_status():
    """Get system status and diagnostics."""
    try:
        db_stats = {
            "connected": False,
            "contacts": 0,
            "cases": 0,
            "tasks": 0,
            "events": 0,
            "users": 0,
            "deadlines": 0
        }
        
        try:
            db_stats["connected"] = True
            db_stats["contacts"] = db.session.query(func.count(Contact.id)).scalar() or 0
            db_stats["cases"] = db.session.query(func.count(Case.id)).scalar() or 0
            db_stats["tasks"] = db.session.query(func.count(Task.id)).scalar() or 0
            db_stats["events"] = db.session.query(func.count(Event.id)).scalar() or 0
            db_stats["users"] = db.session.query(func.count(User.id)).scalar() or 0
            db_stats["deadlines"] = db.session.query(func.count(Deadline.id)).scalar() or 0
        except Exception as e:
            logger.error(f"Database stats error: {str(e)}")
            db_stats["error"] = str(e)
        
        chatbot_status = {
            "healthy": False,
            "base_url": os.getenv("CHATBOT_BASE_URL", "http://localhost:5001"),
            "error": None
        }
        
        try:
            chatbot = ChatbotClient(base_url=chatbot_status["base_url"])
            result = chatbot.health_check()
            chatbot_status["healthy"] = result["success"]
            if not result["success"]:
                chatbot_status["error"] = result["error"]
            chatbot.close()
        except Exception as e:
            logger.error(f"Chatbot status check failed: {str(e)}")
            chatbot_status["error"] = str(e)
        
        env_config = {
            "environment": os.getenv("FLASK_ENV", "development"),
            "debug": os.getenv("FLASK_DEBUG", "False").lower() == "true",
            "database_type": "postgresql" if "postgresql" in os.getenv("DATABASE_URL", "") else "sqlite",
            "webhook_enabled": os.getenv("WEBHOOK_ENABLED", "True").lower() == "true"
        }
        
        return jsonify({
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat(),
            "database": db_stats,
            "chatbot_service": chatbot_status,
            "configuration": env_config
        }), 200
    
    except Exception as e:
        logger.exception(f"Error in admin_status: {str(e)}")
        return jsonify({"status": "error", "error": str(e)}), 500


@admin_bp.post("/load-demo")
def load_demo_data():
    """Load demo data into the CRM for testing."""
    env = os.getenv("FLASK_ENV", "development")
    force = request.args.get("force", "false").lower() == "true"
    
    if env == "production" and not force:
        return jsonify({
            "error": "Demo data loading disabled in production"
        }), 403
    
    try:
        created_count = 0
        
        demo_contacts = [
            {"firstname": "Alice", "lastname": "Johnson", "email": "alice@example.com", "phone": "+1-555-0101", "company": "Tech Corp"},
            {"firstname": "Bob", "lastname": "Smith", "email": "bob@example.com", "phone": "+1-555-0102", "company": "Finance Inc"},
            {"firstname": "Carol", "lastname": "Williams", "email": "carol@example.com", "phone": "+1-555-0103", "company": "Legal Partners"},
            {"firstname": "David", "lastname": "Brown", "email": "david@example.com", "phone": "+1-555-0104", "company": "Healthcare Ltd"},
            {"firstname": "Eve", "lastname": "Davis", "email": "eve@example.com", "phone": "+1-555-0105", "company": "Education Plus"}
        ]
        
        contacts = []
        for contact_data in demo_contacts:
            existing = Contact.query.filter_by(email=contact_data["email"]).first()
            if not existing:
                contact = Contact(**contact_data)
                db.session.add(contact)
                contacts.append(contact)
                created_count += 1
        
        if contacts:
            db.session.flush()
        
        demo_cases = [
            {"title": "Contract Dispute Resolution", "description": "Resolving dispute over service contract terms", "status": "open", "priority": "high", "contactid": contacts[0].id if contacts else None},
            {"title": "Property Claim", "description": "Insurance claim for property damage", "status": "in_progress", "priority": "medium", "contactid": contacts[1].id if len(contacts) > 1 else None},
            {"title": "Employment Matter", "description": "Employee severance negotiation", "status": "pending_review", "priority": "medium", "contactid": contacts[2].id if len(contacts) > 2 else None}
        ]
        
        cases = []
        for case_data in demo_cases:
            if case_data["contactid"]:
                case = Case(**case_data)
                db.session.add(case)
                cases.append(case)
                created_count += 1
        
        if cases:
            db.session.flush()
        
        if cases:
            for i, case in enumerate(cases):
                for j in range(3 if i == 0 else 2):
                    task = Task(
                        caseid=case.id,
                        title=f"Task {j+1} for {case.title}",
                        description=f"Action item related to {case.title}",
                        status="open" if j == 0 else "pending",
                        priority="high" if j == 0 else "medium",
                        due_date=datetime.utcnow() + timedelta(days=7*(j+1))
                    )
                    db.session.add(task)
                    created_count += 1
        
        if cases:
            for case in cases:
                for i in range(2):
                    event = Event(
                        caseid=case.id,
                        title=f"Meeting with {case.title.split()[0]}",
                        description=f"Discussion regarding {case.title}",
                        date=datetime.utcnow() + timedelta(days=14+i),
                        event_type="meeting",
                        location="Conference Room A" if i == 0 else "Virtual"
                    )
                    db.session.add(event)
                    created_count += 1
        
        if cases:
            deadlines_data = [
                {"label": "Filing Deadline", "days": 7},
                {"label": "Response Deadline", "days": 14},
                {"label": "Discovery Cutoff", "days": 30}
            ]
            for case in cases[:2]:
                for deadline_data in deadlines_data:
                    deadline = Deadline(
                        caseid=case.id,
                        label=deadline_data["label"],
                        deadline=datetime.utcnow() + timedelta(days=deadline_data["days"])
                    )
                    db.session.add(deadline)
                    created_count += 1
        
        db.session.commit()
        logger.info(f"Demo data loaded: {created_count} items created")
        
        return jsonify({
            "success": True,
            "message": "Demo data loaded successfully",
            "created_count": created_count,
            "items": {
                "contacts": len([c for c in contacts if c.id]),
                "cases": len([c for c in cases if c.id]),
            },
            "warning": "Demo data is for testing only"
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error loading demo data: {str(e)}")
        return jsonify({"error": "Failed to load demo data", "details": str(e)}), 500


@admin_bp.get("/config")
def admin_config():
    """Get sanitized configuration for admin panel."""
    try:
        config = {
            "environment": os.getenv("FLASK_ENV", "development"),
            "debug": os.getenv("FLASK_DEBUG", "False").lower() == "true",
            "admin_email": os.getenv("ADMIN_EMAIL", "admin@example.com"),
            "database": {
                "type": "postgresql" if "postgresql" in os.getenv("DATABASE_URL", "") else "sqlite",
            },
            "services": {
                "chatbot": os.getenv("CHATBOT_BASE_URL", "http://localhost:5001"),
            },
            "features": {
                "chatbot_enabled": True,
                "webhooks_enabled": os.getenv("WEBHOOK_ENABLED", "True").lower() == "true",
                "demo_mode": os.getenv("FLASK_ENV", "development") != "production"
            }
        }
        
        return jsonify(config), 200
    
    except Exception as e:
        logger.exception(f"Error in admin_config: {str(e)}")
        return jsonify({"error": str(e)}), 500
