from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from ..extensions import db
from ..models.user import User
from ..utils import standardize_error_response

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
limiter = Limiter(key_func=get_remote_address)

@auth_bp.post('/login')
@limiter.limit("5 per minute")
def login():
    """Login with email and password - rate limited to 5/min"""
    data = request.get_json()
    
    if not data:
        return standardize_error_response("No data provided", "NO_DATA", status_code=400)
    
    if not data.get('email') or not data.get('password'):
        return standardize_error_response(
            "Email and password are required", "MISSING_FIELDS",
            field="email" if not data.get('email') else "password",
            status_code=400
        )
    
    user = User.query.filter_by(email=data.get('email'), is_deleted=False).first()
    
    if not user or not user.check_password(data.get('password')):
        return standardize_error_response(
            "Invalid email or password", "INVALID_CREDENTIALS", status_code=401
        )
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.get('/me')
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id, is_deleted=False).first()
    
    if not user:
        return standardize_error_response("User not found", "NOT_FOUND", status_code=404)
    
    return jsonify(user.to_dict()), 200
