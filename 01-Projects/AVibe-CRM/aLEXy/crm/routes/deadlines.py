from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.deadline import Deadline
from ..models.case import Case
from ..schemas import DeadlineSchema
from ..utils import standardize_error_response
from datetime import datetime
from marshmallow import ValidationError

deadlines_bp = Blueprint('deadlines', __name__, url_prefix='/api/deadlines')
deadline_schema = DeadlineSchema()
deadlines_schema = DeadlineSchema(many=True)

@deadlines_bp.get('/')
@jwt_required()
def get_deadlines():
    """List all deadlines with pagination, filtering, sorting"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    caseid = request.args.get('caseid', None, type=int)
    sort = request.args.get('sort', 'date')
    order = request.args.get('order', 'asc')
    
    # Validate pagination
    if page < 1 or per_page < 1 or per_page > 100:
        return standardize_error_response(
            "Invalid pagination parameters", "INVALID_PAGINATION", status_code=400
        )
    
    query = Deadline.query.filter_by(is_deleted=False)
    
    # Apply filtering
    if caseid:
        query = query.filter_by(caseid=caseid)
    
    # Apply sorting
    if sort == 'date':
        query = query.order_by(Deadline.date.asc() if order == 'asc' else Deadline.date.desc())
    elif sort == 'deadline_type':
        query = query.order_by(Deadline.deadline_type.asc() if order == 'asc' else Deadline.deadline_type.desc())
    elif sort == 'createdat':
        query = query.order_by(Deadline.createdat.asc() if order == 'asc' else Deadline.createdat.desc())
    else:
        query = query.order_by(Deadline.createdat.desc())
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "items": [d.to_dict() for d in paginated.items],
        "page": page,
        "per_page": per_page,
        "total": paginated.total,
        "pages": paginated.pages
    }), 200

@deadlines_bp.get('/<int:deadline_id>')
@jwt_required()
def get_deadline(deadline_id):
    """Get single deadline"""
    deadline = Deadline.query.filter_by(id=deadline_id, is_deleted=False).first()
    if not deadline:
        return standardize_error_response("Deadline not found", "NOT_FOUND", status_code=404)
    return jsonify(deadline.to_dict()), 200

@deadlines_bp.post('/')
@jwt_required()
def create_deadline():
    """Create new deadline"""
    data = request.get_json()
    
    if not data:
        return standardize_error_response("No data provided", "NO_DATA", status_code=400)
    
    try:
        validation_result = deadline_schema.load(data)
    except ValidationError as err:
        return standardize_error_response(
            str(err.messages), "VALIDATION_ERROR", 
            field=list(err.messages.keys())[0] if err.messages else None,
            status_code=422
        )
    
    # Verify case exists
    case = Case.query.filter_by(id=validation_result['caseid'], is_deleted=False).first()
    if not case:
        return standardize_error_response("Case not found", "CASE_NOT_FOUND", status_code=404)
    
    deadline = Deadline(
        caseid=validation_result['caseid'],
        date=validation_result['date'],
        deadline_type=validation_result.get('deadline_type'),
        description=validation_result.get('description')
    )
    
    db.session.add(deadline)
    db.session.commit()
    return jsonify(deadline.to_dict()), 201

@deadlines_bp.put('/<int:deadline_id>')
@jwt_required()
def update_deadline(deadline_id):
    """Update deadline"""
    deadline = Deadline.query.filter_by(id=deadline_id, is_deleted=False).first()
    if not deadline:
        return standardize_error_response("Deadline not found", "NOT_FOUND", status_code=404)
    
    data = request.get_json()
    if not data:
        return standardize_error_response("No data provided", "NO_DATA", status_code=400)
    
    try:
        validation_result = deadline_schema.load(data, partial=True)
    except ValidationError as err:
        return standardize_error_response(
            str(err.messages), "VALIDATION_ERROR",
            field=list(err.messages.keys())[0] if err.messages else None,
            status_code=422
        )
    
    if 'caseid' in validation_result:
        case = Case.query.filter_by(id=validation_result['caseid'], is_deleted=False).first()
        if not case:
            return standardize_error_response("Case not found", "CASE_NOT_FOUND", status_code=404)
        deadline.caseid = validation_result['caseid']
    
    if 'date' in validation_result:
        deadline.date = validation_result['date']
    if 'deadline_type' in validation_result:
        deadline.deadline_type = validation_result['deadline_type']
    if 'description' in validation_result:
        deadline.description = validation_result['description']
    
    db.session.commit()
    return jsonify(deadline.to_dict()), 200

@deadlines_bp.delete('/<int:deadline_id>')
@jwt_required()
def delete_deadline(deadline_id):
    """Soft delete deadline"""
    deadline = Deadline.query.filter_by(id=deadline_id, is_deleted=False).first()
    if not deadline:
        return standardize_error_response("Deadline not found", "NOT_FOUND", status_code=404)
    
    deadline.is_deleted = True
    deadline.deleted_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"message": "Deadline deleted", "id": deadline_id}), 200
