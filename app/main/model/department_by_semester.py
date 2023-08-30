from .. import db
from .department import Department
from .semester import Semester

class Department_by_semester(db.Model):
    __tablename__ = 'Department_by_semester'

    semester_key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    semester = db.Column(db.String(10), nullable=False)
    department_key = db.Column(db.String(10), nullable=False)
    number_of_working_students = db.Column(db.Integer, nullable=False)

    department_relationship = db.ForeignKey(department_key, Department.department_code)
    semester_relationship = db.ForeignKey(semester, Semester.working_semester_year)
