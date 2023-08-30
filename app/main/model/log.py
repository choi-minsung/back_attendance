from .. import db
from .user import User
from .department import Department
from .attendance import Attendance_Register

class Log(db.Model):
    __tablename__='Log'

    Logging_key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Logging_text = db.Column(db.Text, nullable=False)
    Logging_time = db.Column(db.String(17), nullable=False)
    attendance_key = db.Column(db.Integer, nullable=False)
    department_number = db.Column(db.String(10), nullable=False)
    student_number = db.Column(db.String(9), nullable=False)

    department_relationship = db.ForeignKey(department_number, Department.department_code)
    user_relationship = db.ForeignKey(student_number, User.student_id)
    attendance_relationship = db.ForeignKey(attendance_key, Attendance_Register.attendance_key)
