from .. import db
from .user import User
from .department import Department

class Semester(db.Model):
    __tablename__ = 'Semester'

    semester_key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    working_semester_year = db.Column(db.String(10), nullable=False)
    student_number = db.Column(db.String(9), nullable=False)
    department_number = db.Column(db.String(10), nullable=False)

    department_relationship = db.ForeignKey(department_number, Department.department_code)
    user_relationship = db.ForeignKey(student_number, User.student_id)
