from ..extensions import db
from datetime import date

class Case(db.Model):
    __tablename__ = "cases"

    id = db.Column(db.Integer, primary_key=True)
    contactid = db.Column(db.Integer, db.ForeignKey("contacts.id", ondelete="RESTRICT"), nullable=False)
    ownerid = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(255), nullable=False)
    casetype = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Intake")
    priority = db.Column(db.String(20), nullable=False, default="Medium")
    openedat = db.Column(db.Date, nullable=False, default=date.today)
    duedate = db.Column(db.Date, nullable=True)
    assignedto = db.Column(db.Integer, nullable=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    createdat = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updatedat = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    contact = db.relationship("Contact", backref=db.backref("cases", lazy=True, passive_deletes=True))

    def to_dict(self):
        return {
            "id": self.id,
            "contactid": self.contactid,
            "ownerid": self.ownerid,
            "title": self.title,
            "casetype": self.casetype,
            "status": self.status,
            "priority": self.priority,
            "openedat": self.openedat.isoformat() if self.openedat else None,
            "duedate": self.duedate.isoformat() if self.duedate else None,
            "assignedto": self.assignedto,
            "is_deleted": self.is_deleted,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "createdat": self.createdat.isoformat() if self.createdat else None,
            "updatedat": self.updatedat.isoformat() if self.updatedat else None
        }
