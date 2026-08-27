from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.task import Task
from ..models.case import Case
from ..models.user import User
from ..schemas import TaskSchema
from ..utils import standardize_error_response
from datetime import datetime
from marshmallow import ValidationError

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@tasks_bp.get('/')
@jwt_required()
def get_tasks():
    """List all tasks with pagination, filtering, sorting"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', None, type=str)
    priority = request.args.get('priority', None, type=str)
    caseid = request.args.get('caseid', None, type=int)
    userid = request.args.get('userid', None, type=int)
    sort = request.args.get('sort', 'createdat')
    order = request.args.get('order', 'desc')
    
    # Validate pagination
    if page < 1 or per_page < 1 or per_page > 100:
        return standardize_error_response(
            "Invalid pagination parameters", "INVALID_PAGINATION", status_code=400
        )
    
    query = Task.query.filter_by(is_deleted=False)
    
    # Apply filtering
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if caseid:
        query = query.filter_by(caseid=caseid)
    if userid:
        query = query.filter_by(userid=userid)
    
    # Apply sorting
    if sort == 'title':
        query = query.order_by(Task.title.asc() if order == 'asc' else Task.title.desc())
    elif sort == 'duedate':
        query = query.order_by(Task.duedate.asc() if order == 'asc' else Task.duedate.desc())
    else:  # createdat default
        query = query.order_by(Task.createdat.asc() if order == 'asc' else Task.createdat.desc())
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "items": [t.to_dict() for t in paginated.items],
        "page": page,
        "per_page": per_page,
        "total": paginated.total,
        "pages": paginated.pages
    }), 200

@tasks_bp.get('/<int:task_id>')
@jwt_required()
def get_task(task_id):
    """Get single task"""
    task = Task.query.filter_by(id=task_id, is_deleted=False).first()
    if not task:
        return standardize_error_response("Task not found", "NOT_FOUND", status_code=404)
    return jsonify(task.to_dict()), 200

@tasks_bp.post('/')
@jwt_required()
def create_task():
    """Create new task with validation"""
    data = request.get_json()
    
    if not data:
        return standardize_error_response("No data provided", "NO_DATA", status_code=400)
    
    try:
        validation_result = task_schema.load(data)
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
    
    # Verify user exists if provided
    if validation_result.get('userid'):
        user = User.query.filter_by(id=validation_result['userid'], is_deleted=False).first()
        if not user:
            return standardize_error_response("User not found", "USER_NOT_FOUND", status_code=404)
    
    task = Task(
        caseid=validation_result['caseid'],
        userid=validation_result.get('userid'),
        title=validation_result['title'],
        description=validation_result.get('description'),
        status=validation_result.get('status', 'pending'),
        priority=validation_result.get('priority', 'Medium'),
        duedate=validation_result.get('duedate')
    )
    
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@tasks_bp.put('/<int:task_id>')
@jwt_required()
def update_task(task_id):
    """Update task"""
    task = Task.query.filter_by(id=task_id, is_deleted=False).first()
    if not task:
        return standardize_error_response("Task not found", "NOT_FOUND", status_code=404)
    
    data = request.get_json()
    if not data:
        return standardize_error_response("No data provided", "NO_DATA", status_code=400)
    
    try:
        validation_result = task_schema.load(data, partial=True)
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
        task.caseid = validation_result['caseid']
    
    if 'userid' in validation_result:
        if validation_result['userid'] is not None:
            user = User.query.filter_by(id=validation_result['userid'], is_deleted=False).first()
            if not user:
                return standardize_error_response("User not found", "USER_NOT_FOUND", status_code=404)
        task.userid = validation_result['userid']
    
    if 'title' in validation_result:
        task.title = validation_result['title']
    if 'description' in validation_result:
        task.description = validation_result['description']
    if 'status' in validation_result:
        task.status = validation_result['status']
    if 'priority' in validation_result:
        task.priority = validation_result['priority']
    if 'duedate' in validation_result:
        task.duedate = validation_result['duedate']
    
    db.session.commit()
    return jsonify(task.to_dict()), 200

@tasks_bp.delete('/<int:task_id>')
@jwt_required()
def delete_task(task_id):
    """Soft delete task"""
    task = Task.query.filter_by(id=task_id, is_deleted=False).first()
    if not task:
        return standardize_error_response("Task not found", "NOT_FOUND", status_code=404)
    
    task.is_deleted = True
    task.deleted_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"message": "Task deleted", "id": task_id}), 200
