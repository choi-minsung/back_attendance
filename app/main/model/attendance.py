from .. import db
from .user import User
from .department import Department
from .semester import Semester


class Attendance_Register(db.Model):
    __tablename__ = "Attendance_register"

    attendance_key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_number = db.Column(db.String(10), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    department_number = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.DateTime, unique=True, nullable=False)
    end_time = db.Column(db.DateTime, unique=True, nullable=True)
    work_text = db.Column(db.Text, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)

    department_relationship = db.ForeignKey(department_number, Department.department_code)
    user_relationship = db.ForeignKey(student_number, User.student_id)
