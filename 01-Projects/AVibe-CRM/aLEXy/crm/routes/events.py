"""
Events API Routes
All endpoints support soft delete and include Marshmallow validation
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from datetime import datetime, timedelta
import logging
from ..extensions import db
from ..models.event import Event
from ..schemas import EventSchema

logger = logging.getLogger(__name__)

events_bp = Blueprint('events', __name__, url_prefix='/api/events')

event_schema = EventSchema()
events_schema = EventSchema(many=True)


@events_bp.route('', methods=['GET'])
def get_events():
    """
    Retrieve paginated list of events with optional filtering.
    
    Query Parameters:
    - page (int): Page number (default: 1)
    - per_page (int): Items per page (default: 10, max: 100)
    - caseid (int): Filter by case ID
    - start_date (str): Filter by start date (ISO format)
    - end_date (str): Filter by end date (ISO format)
    - event_type (str): Filter by event type
    
    Returns:
    {
        "events": [...],
        "pagination": {
            "page": 1,
            "per_page": 10,
            "total": 50,
            "pages": 5
        }
    }
    """
    try:
        page = max(1, int(request.args.get('page', 1)))
        per_page = min(100, max(1, int(request.args.get('per_page', 10))))
        
        query = Event.query.filter_by(is_deleted=False)
        
        # Filter by case ID
        caseid = request.args.get('caseid')
        if caseid:
            query = query.filter_by(caseid=int(caseid))
        
        # Filter by date range
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date:
            start = datetime.fromisoformat(start_date)
            query = query.filter(Event.date >= start)
        if end_date:
            end = datetime.fromisoformat(end_date)
            query = query.filter(Event.date <= end)
        
        # Filter by event type
        event_type = request.args.get('event_type')
        if event_type:
            query = query.filter_by(event_type=event_type)
        
        # Pagination
        paginated = query.order_by(Event.date.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            "events": events_schema.dump(paginated.items),
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": paginated.total,
                "pages": paginated.pages
            }
        }), 200
        
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid query parameters: {str(e)}")
        return jsonify({
            "error": "Invalid query parameters",
            "code": "INVALID_PARAMS",
            "field": None,
            "timestamp": datetime.utcnow().isoformat()
        }), 400


@events_bp.route('', methods=['POST'])
def create_event():
    """
    Create a new event.
    
    Request Body:
    {
        "caseid": 1,
        "title": "Court hearing",
        "description": "Initial hearing",
        "date": "2026-08-15T14:00:00",
        "location": "Court Room 101",
        "event_type": "hearing"
    }
    
    Returns:
    {
        "id": 1,
        "caseid": 1,
        "title": "Court hearing",
        ...
    }
    """
    try:
        data = request.get_json(silent=True) or {}
        
        # Validate request data
        validated_data = event_schema.load(data)
        
        # Create event
        event = Event(
            caseid=validated_data['caseid'],
            title=validated_data['title'],
            description=validated_data.get('description'),
            date=validated_data['date'],
            location=validated_data.get('location'),
            event_type=validated_data.get('event_type')
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify(event_schema.dump(event)), 201
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e.messages)}")
        return jsonify({
            "error": "Validation failed",
            "code": "VALIDATION_ERROR",
            "field": list(e.messages.keys())[0] if e.messages else None,
            "timestamp": datetime.utcnow().isoformat()
        }), 400
    except Exception as e:
        logger.error(f"Error creating event: {str(e)}")
        db.session.rollback()
        return jsonify({
            "error": "Failed to create event",
            "code": "CREATE_ERROR",
            "field": None,
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """
    Retrieve a specific event by ID.
    
    Returns:
    {
        "id": 1,
        "caseid": 1,
        "title": "Court hearing",
        ...
    }
    """
    try:
        event = Event.query.filter(
            Event.id == event_id,
            Event.is_deleted == False
        ).first()
        
        if not event:
            return jsonify({
                "error": "Event not found",
                "code": "NOT_FOUND",
                "field": None,
                "timestamp": datetime.utcnow().isoformat()
            }), 404
        
        return jsonify(event_schema.dump(event)), 200
        
    except Exception as e:
        logger.error(f"Error retrieving event: {str(e)}")
        return jsonify({
            "error": "Failed to retrieve event",
            "code": "RETRIEVE_ERROR",
            "field": None,
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@events_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """
    Update a specific event by ID.
    
    Request Body (all fields optional):
    {
        "title": "Updated title",
        "description": "Updated description",
        "date": "2026-08-15T14:00:00",
        "location": "New location",
        "event_type": "hearing"
    }
    
    Returns:
    {
        "id": 1,
        "caseid": 1,
        "title": "Updated title",
        ...
    }
    """
    try:
        event = Event.query.filter(
            Event.id == event_id,
            Event.is_deleted == False
        ).first()
        
        if not event:
            return jsonify({
                "error": "Event not found",
                "code": "NOT_FOUND",
                "field": None,
                "timestamp": datetime.utcnow().isoformat()
            }), 404
        
        data = request.get_json(silent=True) or {}
        
        # Validate request data (allow partial updates)
        validated_data = event_schema.load(data, partial=True)
        
        # Update fields
        if 'title' in validated_data:
            event.title = validated_data['title']
        if 'description' in validated_data:
            event.description = validated_data['description']
        if 'date' in validated_data:
            event.date = validated_data['date']
        if 'location' in validated_data:
            event.location = validated_data['location']
        if 'event_type' in validated_data:
            event.event_type = validated_data['event_type']
        
        event.updatedat = datetime.utcnow()
        db.session.commit()
        
        return jsonify(event_schema.dump(event)), 200
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e.messages)}")
        return jsonify({
            "error": "Validation failed",
            "code": "VALIDATION_ERROR",
            "field": list(e.messages.keys())[0] if e.messages else None,
            "timestamp": datetime.utcnow().isoformat()
        }), 400
    except Exception as e:
        logger.error(f"Error updating event: {str(e)}")
        db.session.rollback()
        return jsonify({
            "error": "Failed to update event",
            "code": "UPDATE_ERROR",
            "field": None,
            "timestamp": datetime.utcnow().isoformat()
        }), 500


@events_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """
    Soft delete a specific event by ID.
    
    Returns:
    {
        "message": "Event deleted successfully"
    }
    """
    try:
        event = Event.query.filter(
            Event.id == event_id,
            Event.is_deleted == False
        ).first()
        
        if not event:
            return jsonify({
                "error": "Event not found",
                "code": "NOT_FOUND",
                "field": None,
                "timestamp": datetime.utcnow().isoformat()
            }), 404
        
        # Soft delete
        event.is_deleted = True
        event.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": "Event deleted successfully"
        }), 200
        
    except Exception as e:
        logger.error(f"Error deleting event: {str(e)}")
        db.session.rollback()
        return jsonify({
            "error": "Failed to delete event",
            "code": "DELETE_ERROR",
            "field": None,
            "timestamp": datetime.utcnow().isoformat()
        }), 500
