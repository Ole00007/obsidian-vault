from ..extensions import db
from datetime import datetime

class CaseParticipant(db.Model):
    __tablename__ = "case_participants"

    id = db.Column(db.Integer, primary_key=True)
    caseid = db.Column(db.Integer, db.ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    contactid = db.Column(db.Integer, db.ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False)
    role = db.Column(db.String(100), nullable=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    createdat = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updatedat = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    case = db.relationship("Case", backref=db.backref("participants", lazy=True, passive_deletes=True))
    contact = db.relationship("Contact", backref=db.backref("case_participants", lazy=True, passive_deletes=True))

    def to_dict(self):
        return {
            "id": self.id,
            "caseid": self.caseid,
            "contactid": self.contactid,
            "role": self.role,
            "is_deleted": self.is_deleted,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "createdat": self.createdat.isoformat() if self.createdat else None,
            "updatedat": self.updatedat.isoformat() if self.updatedat else None
        }
