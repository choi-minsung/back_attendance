from .. import db

class Department(db.Model):
    __tablename__ = "Department"

    department_code = db.Column(db.String(10), primary_key=True)
    department_name = db.Column(db.String(100))
