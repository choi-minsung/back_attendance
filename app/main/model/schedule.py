from .. import db
from .department import Department
from .user import User

class Schedule(db.Model):
    __tablename__='Schedule'

    Schedule_key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_number = db.Column(db.String(10), nullable=False)
    student_number = db.Column(db.String(9), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    work_start_time = db.Column(db.String(10), nullable=False)
    work_end_time = db.Column(db.String(10), nullable=False)

    department_relationship = db.ForeignKey(department_number, Department.department_code)
    user_relationship = db.ForeignKey(student_number, User.student_id)
