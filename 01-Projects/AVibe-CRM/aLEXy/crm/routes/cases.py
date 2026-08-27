from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models.case import Case
from ..models.contact import Contact
from ..schemas import CaseSchema
from ..utils import standardize_error_response
from datetime import date, datetime
from marshmallow import ValidationError

cases_bp = Blueprint("cases", __name__, url_prefix="/api/cases")
case_schema = CaseSchema()
cases_schema = CaseSchema(many=True)

@cases_bp.get("/")
def get_cases():
    """List all cases with pagination, filtering, sorting"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', None, type=str)
    priority = request.args.get('priority', None, type=str)
    lawyer_id = request.args.get('lawyer_id', None, type=int)
    sort = request.args.get('sort', 'createdat')
    order = request.args.get('order', 'desc')
    
    # Validate pagination
    if page < 1 or per_page < 1 or per_page > 100:
        return standardize_error_response(
            "Invalid pagination parameters", "INVALID_PAGINATION", status_code=400
        )
    
    query = Case.query.filter_by(is_deleted=False)
    
    # Apply filtering
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if lawyer_id:
        query = query.filter_by(assignedto=lawyer_id)
    
    # Apply sorting
    if sort == 'title':
        query = query.order_by(Case.title.asc() if order == 'asc' else Case.title.desc())
    elif sort == 'openedat':
        query = query.order_by(Case.openedat.asc() if order == 'asc' else Case.openedat.desc())
    elif sort == 'duedate':
        query = query.order_by(Case.duedate.asc() if order == 'asc' else Case.duedate.desc())
    else:  # createdat default
        query = query.order_by(Case.createdat.asc() if order == 'asc' else Case.createdat.desc())
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "items": [c.to_dict() for c in paginated.items],
        "page": page,
        "per_page": per_page,
        "total": paginated.total,
        "pages": paginated.pages
    }), 200

@cases_bp.get("/<int:case_id>")
def get_case(case_id):
    """Get single case"""
    case = Case.query.filter_by(id=case_id, is_deleted=False).first()
    if not case:
        return standardize_error_response("Case not found", "NOT_FOUND", status_code=404)
    return jsonify(case.to_dict()), 200

@cases_bp.post("/")
def create_case():
    """Create new case with validation"""
    data = request.get_json()
    
    if not data:
        return standardize_error_response("No data provided", "NO_DATA", status_code=400)
    
    try:
        validation_result = case_schema.load(data)
    except ValidationError as err:
        return standardize_error_response(
            str(err.messages), "VALIDATION_ERROR",
            field=list(err.messages.keys())[0] if err.messages else None,
            status_code=422
        )
    
    # Verify contact exists
    contact = Contact.query.filter_by(id=validation_result['contactid'], is_deleted=False).first()
    if not contact:
        return standardize_error_response("Contact not found", "CONTACT_NOT_FOUND", status_code=404)
    
    case = Case(
        contactid=validation_result['contactid'],
        ownerid=validation_result.get('ownerid'),
        title=validation_result['title'],
        casetype=validation_result.get('casetype'),
        status=validation_result.get('status', "Intake"),
        priority=validation_result.get('priority', "Medium"),
        openedat=validation_result.get('openedat') or date.today(),
        duedate=validation_result.get('duedate'),
        assignedto=validation_result.get('assignedto')
    )
    
    db.session.add(case)
    db.session.commit()
    return jsonify(case.to_dict()), 201

@cases_bp.put("/<int:case_id>")
def update_case(case_id):
    """Update case"""
    case = Case.query.filter_by(id=case_id, is_deleted=False).first()
    if not case:
        return standardize_error_response("Case not found", "NOT_FOUND", status_code=404)
    
    data = request.get_json()
    if not data:
        return standardize_error_response("No data provided", "NO_DATA", status_code=400)
    
    try:
        validation_result = case_schema.load(data, partial=True)
    except ValidationError as err:
        return standardize_error_response(
            str(err.messages), "VALIDATION_ERROR",
            field=list(err.messages.keys())[0] if err.messages else None,
            status_code=422
        )
    
    if 'contactid' in validation_result:
        contact = Contact.query.filter_by(id=validation_result['contactid'], is_deleted=False).first()
        if not contact:
            return standardize_error_response("Contact not found", "CONTACT_NOT_FOUND", status_code=404)
        case.contactid = validation_result['contactid']
    
    if 'title' in validation_result:
        case.title = validation_result['title']
    if 'casetype' in validation_result:
        case.casetype = validation_result['casetype']
    if 'status' in validation_result:
        case.status = validation_result['status']
    if 'priority' in validation_result:
        case.priority = validation_result['priority']
    if 'openedat' in validation_result:
        case.openedat = validation_result['openedat']
    if 'duedate' in validation_result:
        case.duedate = validation_result['duedate']
    if 'assignedto' in validation_result:
        case.assignedto = validation_result['assignedto']
    if 'ownerid' in validation_result:
        case.ownerid = validation_result['ownerid']
    
    db.session.commit()
    return jsonify(case.to_dict()), 200

@cases_bp.delete("/<int:case_id>")
def delete_case(case_id):
    """Soft delete case"""
    case = Case.query.filter_by(id=case_id, is_deleted=False).first()
    if not case:
        return standardize_error_response("Case not found", "NOT_FOUND", status_code=404)
    
    case.is_deleted = True
    case.deleted_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"message": "Case deleted", "id": case_id}), 200
