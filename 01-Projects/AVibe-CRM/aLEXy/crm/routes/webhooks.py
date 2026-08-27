"""Webhook handlers for chatbot events and Netlify notifications."""
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.event import Event
from ..models.case import Case
from ..clients.chatbot import ChatbotClient
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)
webhooks_bp = Blueprint("webhooks", __name__, url_prefix="/webhooks")

chatbot_client = None

def get_chatbot_client():
    """Get or create chatbot client instance."""
    global chatbot_client
    if chatbot_client is None:
        base_url = os.getenv("CHATBOT_BASE_URL", "http://localhost:5001")
        chatbot_client = ChatbotClient(base_url=base_url)
    return chatbot_client


@webhooks_bp.post("/chatbot/message")
def handle_chatbot_message():
    """Handle chatbot message webhook."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON payload"}), 400
        
        required_fields = ["user_id", "case_id", "message"]
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
        
        user_id = data.get("user_id")
        case_id = data.get("case_id")
        message = data.get("message")
        response = data.get("response", "")
        
        case = Case.query.get(case_id)
        if not case:
            logger.warning(f"Webhook: Case {case_id} not found")
            return jsonify({"error": "Case not found"}), 404
        
        event_title = f"Chatbot Message from User {user_id}"
        event_description = f"User: {message}\nChatbot: {response}"
        
        event = Event(
            caseid=case_id,
            title=event_title,
            description=event_description,
            date=datetime.utcnow(),
            event_type="chatbot_message",
            location=None
        )
        
        db.session.add(event)
        db.session.commit()
        
        logger.info(f"Chatbot message event created: {event.id} for case {case_id}")
        
        return jsonify({
            "success": True,
            "event_id": event.id,
            "message": "Chatbot message logged successfully"
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error handling chatbot message webhook: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@webhooks_bp.post("/chatbot/sentiment")
def handle_chatbot_sentiment():
    """Handle chatbot sentiment analysis webhook."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON payload"}), 400
        
        case_id = data.get("case_id")
        sentiment = data.get("sentiment", "neutral")
        confidence = data.get("confidence", 0)
        message = data.get("message", "")
        
        case = Case.query.get(case_id)
        if not case:
            logger.warning(f"Webhook: Case {case_id} not found for sentiment")
            return jsonify({"error": "Case not found"}), 404
        
        event = Event(
            caseid=case_id,
            title=f"Sentiment Analysis: {sentiment.capitalize()}",
            description=f"Sentiment: {sentiment} (confidence: {confidence:.2f})\nMessage: {message}",
            date=datetime.utcnow(),
            event_type="sentiment_analysis",
            location=None
        )
        
        db.session.add(event)
        db.session.commit()
        
        logger.info(f"Sentiment event created: {event.id} - {sentiment} ({confidence})")
        
        return jsonify({
            "success": True,
            "event_id": event.id,
            "message": "Sentiment analysis logged"
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error handling sentiment webhook: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@webhooks_bp.post("/netlify/deploy")
def handle_netlify_deploy():
    """Handle Netlify deployment notifications."""
    try:
        data = request.get_json()
        
        if not data:
            logger.info("Netlify webhook: No payload, responding with 200")
            return jsonify({"success": True}), 200
        
        build_id = data.get("id", "unknown")
        state = data.get("state", "unknown")
        url = data.get("url", "")
        commit_msg = data.get("commit", {}).get("message", "No message")
        
        logger.info(f"Netlify deployment: {build_id} - {state}")
        logger.info(f"  URL: {url}")
        logger.info(f"  Commit: {commit_msg}")
        
        if state == "error":
            logger.warning(f"Netlify build failed: {build_id}")
        
        return jsonify({
            "success": True,
            "build_id": build_id,
            "message": "Deployment notification received"
        }), 200
    
    except Exception as e:
        logger.exception(f"Error handling Netlify webhook: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@webhooks_bp.get("/health")
def webhook_health():
    """Health check for webhook system."""
    return jsonify({
        "status": "ok",
        "webhooks": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }), 200
