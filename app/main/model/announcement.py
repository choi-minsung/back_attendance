from .. import db
from .user import User
from .department import Department
from datetime import datetime


class Announcement(db.Model):
    __tablename__ = "Announcement"

    announcement_key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_number = db.Column(db.String(10), nullable=True)
    student_number = db.Column(db.String(9), nullable=False)
    announcement_title = db.Column(db.String(50), nullable=False)
    announcement_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

    department_relationship = db.ForeignKey(
        department_number, Department.department_code
    )
    user_relationship = db.ForeignKey(student_number, User.student_id)
