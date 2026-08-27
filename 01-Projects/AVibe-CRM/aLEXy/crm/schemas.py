from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import date

class ContactSchema(Schema):
    id = fields.Int(dump_only=True)
    ownerid = fields.Int(allow_none=True)
    fullname = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    email = fields.Email(allow_none=True)
    phone = fields.Str(allow_none=True, validate=validate.Length(max=50))
    company = fields.Str(allow_none=True, validate=validate.Length(max=255))
    status = fields.Str(allow_none=True, validate=validate.Length(max=50))
    notes = fields.Str(allow_none=True)
    is_deleted = fields.Bool(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

class CaseSchema(Schema):
    id = fields.Int(dump_only=True)
    contactid = fields.Int(required=True)
    ownerid = fields.Int(allow_none=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    casetype = fields.Str(allow_none=True, validate=validate.Length(max=100))
    status = fields.Str(allow_none=True, validate=validate.Length(max=50))
    priority = fields.Str(allow_none=True, validate=validate.Length(max=20))
    openedat = fields.Date(allow_none=True)
    duedate = fields.Date(allow_none=True)
    assignedto = fields.Int(allow_none=True)
    is_deleted = fields.Bool(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)
    createdat = fields.DateTime(dump_only=True)
    updatedat = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if data.get('openedat') and data.get('duedate'):
            if data['openedat'] > data['duedate']:
                raise ValidationError("duedate must be after openedat")

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    caseid = fields.Int(required=True)
    userid = fields.Int(allow_none=True)
    eventid = fields.Int(allow_none=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    status = fields.Str(allow_none=True, validate=validate.Length(max=50))
    priority = fields.Str(allow_none=True, validate=validate.Length(max=20))
    duedate = fields.Date(allow_none=True)
    is_deleted = fields.Bool(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)
    createdat = fields.DateTime(dump_only=True)
    updatedat = fields.DateTime(dump_only=True)

class DeadlineSchema(Schema):
    id = fields.Int(dump_only=True)
    caseid = fields.Int(required=True)
    date = fields.Date(required=True)
    deadline_type = fields.Str(allow_none=True, validate=validate.Length(max=100))
    description = fields.Str(allow_none=True)
    is_deleted = fields.Bool(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)
    createdat = fields.DateTime(dump_only=True)
    updatedat = fields.DateTime(dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8))
    role = fields.Str(allow_none=True, validate=validate.Length(max=50))
    is_deleted = fields.Bool(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class CaseParticipantSchema(Schema):
    id = fields.Int(dump_only=True)
    caseid = fields.Int(required=True)
    contactid = fields.Int(required=True)
    role = fields.Str(allow_none=True, validate=validate.Length(max=100))
    is_deleted = fields.Bool(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)
    createdat = fields.DateTime(dump_only=True)
    updatedat = fields.DateTime(dump_only=True)

class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    caseid = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    date = fields.DateTime(required=True)
    location = fields.Str(allow_none=True, validate=validate.Length(max=255))
    event_type = fields.Str(allow_none=True, validate=validate.Length(max=100))
    is_deleted = fields.Bool(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)
    createdat = fields.DateTime(dump_only=True)
    updatedat = fields.DateTime(dump_only=True)
