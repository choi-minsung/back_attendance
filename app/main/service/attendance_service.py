import datetime
import calendar
import json
from dateutil.relativedelta import relativedelta
from sqlalchemy import desc

from app.main import db
from app.main.model.attendance import Attendance_Register
from app.main.model.department import Department
from app.main.model.user import User
from app.main.model.log import Log
from typing import Dict, Tuple
from app.main.service.scheduler_service import check_token, valid_token


class Attendance:
    @staticmethod
    def work_start(header: str) -> Tuple[Dict[str, str], int]:
        if header:
            user, department_number = check_token(header)
            response_object, number = work_start_function(user,
                                                          department_number)
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def leave_work(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user, department_number = check_token(header)
            # 퇴근 시간 입력
            response_object, number = work_leave_function(user,
                                                          department_number,
                                                          data)
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def create_attendance(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user, department_number = check_token(header)
            # 퇴근 시간 입력
            response_object, number = create_function(user,
                                                      department_number,
                                                      data)
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def update_attendance(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user, department_number = check_token(header)
            response_object, number = update_attendance_function(user,
                                                                 department_number,
                                                                 data)
            return response_object, number
        else:
            # 토큰이 없는 경우
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def read_attendance(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user, department_number = check_token(header)
            response_object, number = read_attendance_function(user,
                                                               department_number,
                                                               data)
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def delete_attendance(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user, department_number = check_token(header)
            response_object, number = delete_attendance_function(user,
                                                                 department_number,
                                                                 data)
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number


def delete_attendance(data: Attendance_Register):
    db.session.delete(data)
    db.session.commit()


# 해당 데이터 Delete


def save_changes(data: Attendance_Register) -> None:
    db.session.add(data)
    db.session.commit()


# 해당 데이터 Save


def save_changes_log(data: Log) -> None:
    db.session.add(data)
    db.session.commit()


# 해당 데이터 Log Save


def find_semester():
    now = datetime.datetime.utcnow()
    if 2 < now.month < 9:
        return datetime.datetime(now.year, 3, 1, 0, 0, 0), datetime.datetime(now.year, 8, 31, 23, 59, 59)
    else:
        after_one_year = now + relativedelta(year=1)
        if calendar.isleap(after_one_year.year):
            return datetime.datetime(now.year, 9, 1, 0, 0, 0), datetime.datetime(now.year + 1, 2, 29, 23, 59, 59)
        else:
            return datetime.datetime(now.year, 9, 1, 0, 0, 0), datetime.datetime(now.year + 1, 2, 28, 23, 59, 59)


# 1학기인지 2학기인지 찾아서 리턴


def work_start_function(user, department_number):
    # DBMS에게 데이터 넘겨주는 코드
    work_start_time = datetime.datetime.now()
    work_start_time = work_start_time.strftime("%Y-%m-%d %H:%M")
    new_attendance = Attendance_Register(
        student_number=user.student_id,
        user_name=user.username,
        department_number=department_number.department_number,
        start_time=work_start_time,
        registered_on=work_start_time
    )
    save_changes(new_attendance)
    # 로그를 저장하기 위한 코드
    new_attendance_log = Log(
        student_number=user.student_id,
        Logging_text="student work start.",
        Logging_time=work_start_time,
        attendance_key=new_attendance.attendance_key,
        department_number=department_number.department_number
    )
    save_changes_log(new_attendance_log)
    # 프론트에게 넘기기 위한 코드
    response_object = {
        'status': 'success',
        'work_start_time': work_start_time
    }

    return response_object, 200


# 버튼을 누르면 새로 하나 만든 후 저장


def work_leave_function(user, department_number, data):
    # 유저 확인 후 출석부 리턴
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d")
    attendance = Attendance_Register.query.filter(
        Attendance_Register.student_number == user.student_id,
        Attendance_Register.department_number == department_number.department_number,
        Attendance_Register.start_time.like(str(now) + '%'),
        Attendance_Register.end_time == None
    ).first()
    leave_time = datetime.datetime.now()
    leave_time = leave_time.strftime("%Y-%m-%d %H:%M")
    # 퇴근 시간 입력
    attendance.end_time = leave_time
    attendance.registered_on = leave_time
    attendance.work_text = data['work_text']
    db.session.commit()
    print(attendance)
    # 로그 찍기
    new_attendance_log = Log(
        student_number=user.student_id,
        Logging_text="student work end.",
        Logging_time=leave_time,
        attendance_key=attendance.attendance_key,
        department_number=department_number.department_number
    )
    save_changes_log(new_attendance_log)

    # 프론트에게 리턴
    response_object = {
        'status': 'success',
        'work_start_time': attendance.start_time.strftime("%Y-%m-%d %H:%M"),
        'work_end_time': leave_time,
        'work text': attendance.work_text
    }
    return response_object, 200


# 퇴근 시 퇴근시간 변경 후 저장


def create_function(user, department_number, data):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    if user.user_group == 2:
        # 부서 관리자인 것이 확인되면 생성으로 넘어감
        new_attendance = Attendance_Register(
            student_id=data['student_id'],
            department_number=department_number.department_code,
            start_time=data['start_time'],
            end_time=data['end_time'],
            registered_on=now
        )
        save_changes(new_attendance)
        # 생성 후 로그 찍기
        new_attendance_log = Log(
            student_number=user.student_id,
            Logging_text="manager create attendance.",
            Logging_time=now,
            attendance_key=new_attendance.attendance_key,
            department_number=department_number.department_code
        )
        save_changes_log(new_attendance_log)

        response_object = {
            'status': 'success',
            'message': now
        }
        return response_object, 200
    elif user.user_group == 1:
        # 총괄 관리자인 경우
        department = Department.query.filter(
            Department.department_name == data['department_name']
        ).first()
        print(department.department_name)
        student = User.query.filter(
            User.student_id == data['student_id']
        ).first()
        # 전체 관리자인 것이 확인되면 생성으로 넘어감
        new_attendance = Attendance_Register(
            student_number=data['student_id'],
            user_name=student.username,
            department_number=department.department_code,
            start_time=data['start_time'],
            end_time=data['end_time'],
            work_text=data['work_text'],
            registered_on=now
        )
        save_changes(new_attendance)
        # 생성 후 로그 찍기
        new_attendance_log = Log(
            student_number=user.student_id,
            Logging_text="manager create attendance.",
            Logging_time=now,
            attendance_key=new_attendance.attendance_key,
            department_number=department.department_code
        )
        save_changes_log(new_attendance_log)

        response_object = {
            'status': 'success',
            'message': now
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'you are not the manager'
        }
        return response_object, 401


def update_attendance_function(user, department_number, data):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    if user.user_group == 2:
        # 부서 관리자
        access_in_attendance = Attendance_Register.query.filter(
            Attendance_Register.department_number == department_number.department_code,
            Attendance_Register.student_number == data['student_id'],
            Attendance_Register.start_time == data['start_time'],
            Attendance_Register.end_time == None
        ).first()
        # 해당 학기 및 해당 부서의 전체 출석부 리턴
        access_in_attendance.end_time = datetime.datetime.strptime(data['update_end_time'], "%Y-%m-%d %H:%M")
        db.session.commit()

        new_attendance_log = Log(
            student_number=user.student_id,
            Logging_text="manager update attendance.",
            Logging_time=now,
            attendance_key=access_in_attendance.attendance_key,
            department_number=access_in_attendance.department_code
        )
        save_changes_log(new_attendance_log)

        # 해당 데이터 찾은 후 변경 리턴
        response_object = {
            'status': 'success',
            'message': 'You update attendance',
            'update data': access_in_attendance.end_time
        }
        return response_object, 200
    elif user.user_group == 3:
        # 학생인 경우
        response_object = {
            'status': 'fail',
            'message': 'You can not access it because you are not an administrator.'
        }
        return response_object, 401
    else:
        # 총괄 관리자인 경우
        department = Department.query.filter(
            Department.department_name == data['department_number']
        ).first()
        # 전체 관리자
        access_in_attendance = Attendance_Register.query.filter(
            Attendance_Register.department_number == department.department_code,
            Attendance_Register.student_number == data['student_id'],
            Attendance_Register.start_time == data['start_time'],
            Attendance_Register.end_time == None
        ).first()
        print(access_in_attendance)
        # 해당 학기 및 해당 부서의 전체 출석부 리턴
        access_in_attendance.end_time = datetime.datetime.strptime(data['update_end_time'], "%Y-%m-%d %H:%M")
        db.session.commit()
        new_attendance_log = Log(
            student_number=user.student_id,
            Logging_text="manager update attendance.",
            Logging_time=now,
            attendance_key=access_in_attendance.attendance_key,
            department_number=access_in_attendance.department_number
        )
        save_changes_log(new_attendance_log)
        # 해당 데이터 찾은 후 변경 리턴
        response_object = {
            'status': 'success',
            'message': 'You update attendance',
            'update data': access_in_attendance.end_time
        }
        return response_object, 200


# 관리자가 직접 퇴근시간 변경 후 저장


def read_attendance_function(user, department_number, data):
    start_semester, end_semester = find_semester()
    if user.user_group == 2:  # 부서 관리자
        access_in_attendance = Attendance_Register.query.filter(
            Attendance_Register.student_number == data['student_id'],
            Attendance_Register.department_number == department_number.department_number,
            Attendance_Register.start_time.between(start_semester, end_semester)
        ).order_by(Attendance_Register.start_time).all()
    elif user.user_group == 3:  # 학생
        access_in_attendance = Attendance_Register.query.filter(
            Attendance_Register.student_number == user.student_id,
            Attendance_Register.department_number == department_number.department_number,
            Attendance_Register.start_time.between(start_semester, end_semester)
        ).order_by(Attendance_Register.start_time).all()
    else:  # 전체 관리자
        department = Department.query.filter(
            Department.department_name == data['department_name']
        ).first()
        access_in_attendance = Attendance_Register.query.filter(
            Attendance_Register.student_number == data['student_id'],
            Attendance_Register.department_number == department.department_code,
            Attendance_Register.start_time.between(start_semester, end_semester)
        ).order_by(Attendance_Register.start_time).all()

    response_object = {
        'status': 'success',
        'data': {
            'student_number': user.student_id if user.user_group == 3 else data['student_id'],
            'scheduler_datas': [
                {
                    'department_number': attendance_data.department_number,
                    'work_start_time': attendance_data.start_time.strftime("%Y-%m-%d %H:%M"),
                    'work_end_time': attendance_data.end_time.strftime("%Y-%m-%d %H:%M") if attendance_data.end_time is not None else None
                } for attendance_data in access_in_attendance
            ]
        }
    }
    return response_object, 200


# 이번 달 근무 시간 찾은 후 리턴


def delete_attendance_function(user, department_number, data):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    if user.user_group == 1:
        department_number = Department.query.filter(
            Department.department_name == data['department_name']
        ).first()
    elif user.user_group == 3:
        data['student_id'] = user.student_id
    access_in_attendance = Attendance_Register.query.filter(
        Attendance_Register.student_number == data['student_id'],
        Attendance_Register.department_number == department_number.department_code,
        Attendance_Register.start_time == data['start_time'],
    ).first()
    new_attendance_log = Log(
        student_number=user.student_id,
        Logging_text="manager delete attendance.",
        Logging_time=now,
        attendance_key=access_in_attendance.attendance_key,
        department_number=access_in_attendance.department_number
    )
    save_changes_log(new_attendance_log)
    delete_attendance(access_in_attendance)
    response_object = {
        'status': 'success',
        'data': {
            'user number': user.student_id,
            'department number': department_number.department_code,
            'start time': data['work_start_time']
        }
    }
    return response_object, 200
# 해당하는 근무 시간 삭제
