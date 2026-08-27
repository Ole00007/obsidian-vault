from ..extensions import db
from datetime import datetime

class Deadline(db.Model):
    __tablename__ = "deadlines"

    id = db.Column(db.Integer, primary_key=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    deadline_type = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    createdat = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updatedat = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    case = db.relationship("Case", backref=db.backref("deadlines", lazy=True, passive_deletes=True))

    def to_dict(self):
        return {
            "id": self.id,
            "caseid": self.caseid,
            "date": self.date.isoformat() if self.date else None,
            "deadline_type": self.deadline_type,
            "description": self.description,
            "is_deleted": self.is_deleted,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "createdat": self.createdat.isoformat() if self.createdat else None,
            "updatedat": self.updatedat.isoformat() if self.updatedat else None
        }
