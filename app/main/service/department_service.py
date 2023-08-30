from app.main import db
from app.main.model.department import Department
from app.main.model.department_by_semester import Department_by_semester
from app.main.model.semester import Semester
from app.main.model.user import User
from typing import Dict, Tuple
from app.main.service.scheduler_service import valid_token, find_semester_schedule


class DepartmentService:
    @staticmethod
    def create_department(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user = check_user(header)
            if user.user_group == 1:
                response_object, number = create_department_function(data)
            else:
                response_object = {
                    'status': 'success',
                    'message': 'Access is not possible because you are not a full administrator.'
                }
                number = 401
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def join_department(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user = check_user(header)
            if user.user_group == 1:
                response_object, number = join_department_function(0,
                                                                   data)
            elif user.user_group == 2:
                department_number = Semester.query.filter(
                    Semester.student_number == user.student_id
                ).first()
                response_object, number = join_department_function(department_number.department_number,
                                                                   data)
            else:
                response_object = {
                    'status': 'success',
                    'message': 'Access is not possible because you are not a administrator.'
                }
                number = 401
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def update_department(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user = check_user(header)
            if user.user_group == 1:
                response_object, number = update_department_function(0,
                                                                     data)
            elif user.user_group == 2:
                department_number = Semester.query.filter(
                    Semester.student_number == user.student_id
                ).frist()
                response_object, number = update_department_function(department_number.department_number,
                                                                     data)
            else:
                response_object = {
                    'status': 'success',
                    'message': 'Access is not possible because you are not a administrator.'
                }
                number = 401
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number


def check_user(auth_token):
    resp = User.decode_auth_token(auth_token)
    user = User.query.filter(User.id == resp).first()
    return user


def save_department_changes(data: Department) -> None:
    db.session.add(data)
    db.session.commit()


def save_department_semester_changes(data: Department_by_semester) -> None:
    db.session.add(data)
    db.session.commit()


def save_semester_changes(data: Semester) -> None:
    db.session.add(data)
    db.session.commit()

def create_department_function(data):
    new_department = Department(
        department_name=data["department_name"],
        department_code=data["department_code"],
    )
    save_department_changes(new_department)
    now = find_semester_schedule()
    new_department_semester = Department_by_semester(
        semester=now,
        department_key=new_department.department_code,
        number_of_working_students=data["number_of_working_students"]
    )
    save_department_semester_changes(new_department_semester)
    response_object = {
        'status': 'success',
        'department number': new_department.department_name
    }
    return response_object, 200


def update_department_function(department_number, data):
    now = find_semester_schedule()
    if department_number == 0:
        department = Department.query.filter(
            Department.department_name == data['department_name']
        ).first()
        department_semester = Department_by_semester.query.filter(
            Department_by_semester.semester == now,
            Department_by_semester.department_key == department.department_code,
        ).first()
        department_semester.number_of_working_students = data["number_of_working_students"]
        db.session.commit()
        response_object = {
            'status': 'success',
            'department number': department.department_code
        }
        return response_object, 200
    else:
        department_semester = Department_by_semester.query.filter(
            Department_by_semester.semester == now,
            Department_by_semester.department_key == department_number,
        ).first()
        department_semester.number_of_working_students = data["number_of_working_students"]
        db.session.commit()
        response_object = {
            'status': 'success',
            'department number': department_semester.department_key
        }
        return response_object, 200


def join_department_function(department_number, data):
    now = find_semester_schedule()
    if department_number == 0:
        department = Department.query.filter(
            Department.department_name == data['department_name']
        ).first()
        department_semester = Department_by_semester.query.filter(
            Department_by_semester.semester == now,
            Department_by_semester.department_key == department.department_code,
        ).first()
        #print(department_semester)
        new_student_join = Semester(
            working_semester_year=department_semester.semester,
            student_number=data['student_id'],
            department_number=department.department_code
        )
        save_semester_changes(new_student_join)
        response_object = {
            'status': 'success',
            'department join student': data['student_id']
        }
        return response_object, 200
    else:
        department_semester = Department_by_semester.query.filter(
            Department_by_semester.semester == now,
            Department_by_semester.department_key == department_number,
        ).first()
        new_student_join = Semester(
            working_semester_year=department_semester.semester,
            student_number=data['student_id'],
            department_number=department_number
        )
        save_semester_changes(new_student_join)
        response_object = {
            'status': 'success',
            'department join student': data['student_id']
        }
        return response_object, 200
