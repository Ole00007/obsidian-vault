from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from ..extensions import db
from ..models.contact import Contact
from ..schemas import ContactSchema
from ..utils import standardize_error_response
from datetime import datetime
from marshmallow import ValidationError

contacts_bp = Blueprint('contacts', __name__, url_prefix='/api/contacts')
contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

@contacts_bp.get('/')
def get_contacts():
    """List all contacts with pagination, filtering, sorting, search"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    q = request.args.get('q', None, type=str)  # Full-text search
    status = request.args.get('status', None, type=str)
    sort = request.args.get('sort', 'fullname')
    order = request.args.get('order', 'asc')
    
    # Validate pagination
    if page < 1 or per_page < 1 or per_page > 100:
        return standardize_error_response(
            "Invalid pagination parameters", "INVALID_PAGINATION", status_code=400
        )
    
    query = Contact.query.filter_by(is_deleted=False)
    
    # Apply full-text search
    if q:
        q_pattern = f"%{q}%"
        query = query.filter(
            db.or_(
                Contact.fullname.ilike(q_pattern),
                Contact.email.ilike(q_pattern),
                Contact.company.ilike(q_pattern),
                Contact.phone.ilike(q_pattern)
            )
        )
    
    # Apply filtering
    if status:
        query = query.filter_by(status=status)
    
    # Apply sorting
    if sort == 'email':
        query = query.order_by(Contact.email.asc() if order == 'asc' else Contact.email.desc())
    elif sort == 'company':
        query = query.order_by(Contact.company.asc() if order == 'asc' else Contact.company.desc())
    elif sort == 'id':
        query = query.order_by(Contact.id.asc() if order == 'asc' else Contact.id.desc())
    else:  # fullname default
        query = query.order_by(Contact.fullname.asc() if order == 'asc' else Contact.fullname.desc())
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "items": [c.to_dict() for c in paginated.items],
        "page": page,
        "per_page": per_page,
        "total": paginated.total,
        "pages": paginated.pages
    }), 200

@contacts_bp.post('/')
def create_contact():
    """Create new contact with validation"""
    data = request.get_json()
    
    if not data:
        return standardize_error_response("No data provided", "NO_DATA", status_code=400)
    
    # Use field from form submission or JSON
    fullname = data.get('full_name') or data.get('fullname')
    
    try:
        validation_result = contact_schema.load({
            'fullname': fullname,
            'email': data.get('email'),
            'phone': data.get('phone'),
            'company': data.get('company'),
            'status': data.get('status', 'lead'),
            'notes': data.get('notes'),
            'ownerid': data.get('ownerid')
        })
    except ValidationError as err:
        return standardize_error_response(
            str(err.messages), "VALIDATION_ERROR",
            field=list(err.messages.keys())[0] if err.messages else None,
            status_code=422
        )
    
    contact = Contact(
        ownerid=validation_result.get('ownerid'),
        fullname=validation_result['fullname'],
        email=validation_result.get('email'),
        phone=validation_result.get('phone'),
        company=validation_result.get('company'),
        status=validation_result.get('status', 'lead'),
        notes=validation_result.get('notes')
    )
    
    db.session.add(contact)
    db.session.commit()
    return jsonify(contact.to_dict()), 201

@contacts_bp.get('/<int:contact_id>')
def get_contact(contact_id):
    """Get single contact"""
    contact = Contact.query.filter_by(id=contact_id, is_deleted=False).first()
    if not contact:
        return standardize_error_response("Contact not found", "NOT_FOUND", status_code=404)
    return jsonify(contact.to_dict()), 200

@contacts_bp.put('/<int:contact_id>')
def update_contact(contact_id):
    """Update contact"""
    contact = Contact.query.filter_by(id=contact_id, is_deleted=False).first()
    if not contact:
        return standardize_error_response("Contact not found", "NOT_FOUND", status_code=404)
    
    data = request.get_json()
    if not data:
        return standardize_error_response("No data provided", "NO_DATA", status_code=400)
    
    try:
        validation_result = contact_schema.load(data, partial=True)
    except ValidationError as err:
        return standardize_error_response(
            str(err.messages), "VALIDATION_ERROR",
            field=list(err.messages.keys())[0] if err.messages else None,
            status_code=422
        )
    
    if 'fullname' in validation_result:
        contact.fullname = validation_result['fullname']
    if 'email' in validation_result:
        contact.email = validation_result['email']
    if 'phone' in validation_result:
        contact.phone = validation_result['phone']
    if 'company' in validation_result:
        contact.company = validation_result['company']
    if 'status' in validation_result:
        contact.status = validation_result['status']
    if 'notes' in validation_result:
        contact.notes = validation_result['notes']
    if 'ownerid' in validation_result:
        contact.ownerid = validation_result['ownerid']
    
    db.session.commit()
    return jsonify(contact.to_dict()), 200

@contacts_bp.delete('/<int:contact_id>')
def delete_contact(contact_id):
    """Soft delete contact"""
    contact = Contact.query.filter_by(id=contact_id, is_deleted=False).first()
    if not contact:
        return standardize_error_response("Contact not found", "NOT_FOUND", status_code=404)
    
    contact.is_deleted = True
    contact.deleted_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"message": "Contact deleted", "id": contact_id}), 200
