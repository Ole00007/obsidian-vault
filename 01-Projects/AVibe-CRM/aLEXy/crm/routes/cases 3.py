from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models.case import Case
from ..models.contact import Contact
from datetime import date

cases_bp = Blueprint("cases", __name__)

@cases_bp.get("/cases")
def get_cases():
    cases = Case.query.order_by(Case.id.desc()).all()
    return jsonify([c.to_dict() for c in cases]), 200

@cases_bp.post("/cases")
def create_case():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not data.get("contactid"):
        return jsonify({"error": "contactid is required"}), 400
    if not data.get("title"):
        return jsonify({"error": "title is required"}), 400

    contact = Contact.query.get(data.get("contactid"))
    if not contact:
        return jsonify({"error": "contact not found"}), 404

    case = Case(
        contactid=data.get("contactid"),
        ownerid=data.get("ownerid"),
        title=data.get("title"),
        casetype=data.get("casetype"),
        status=data.get("status", "Intake"),
        priority=data.get("priority", "Medium"),
        openedat=date.fromisoformat(data["openedat"]) if data.get("openedat") else date.today(),
        duedate=date.fromisoformat(data["duedate"]) if data.get("duedate") else None,
        assignedto=data.get("assignedto")
    )
    db.session.add(case)
    db.session.commit()
    return jsonify(case.to_dict()), 201
