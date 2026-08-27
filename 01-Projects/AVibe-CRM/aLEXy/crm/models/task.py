from ..extensions import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    eventid = db.Column(db.Integer, db.ForeignKey("events.id", ondelete="SET NULL"), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="pending")
    priority = db.Column(db.String(20), nullable=False, default="Medium")
    duedate = db.Column(db.Date, nullable=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    createdat = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updatedat = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    case = db.relationship("Case", backref=db.backref("tasks", lazy=True, passive_deletes=True))
    user = db.relationship("User", backref=db.backref("tasks", lazy=True, passive_deletes=True))
    event = db.relationship("Event", backref=db.backref("tasks", lazy=True, passive_deletes=True))

    def to_dict(self):
        return {
            "id": self.id,
            "caseid": self.caseid,
            "userid": self.userid,
            "eventid": self.eventid,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "duedate": self.duedate.isoformat() if self.duedate else None,
            "is_deleted": self.is_deleted,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "createdat": self.createdat.isoformat() if self.createdat else None,
            "updatedat": self.updatedat.isoformat() if self.updatedat else None
        }
