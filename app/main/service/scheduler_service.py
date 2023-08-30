import datetime
from app.main import db
from app.main.model.schedule import Schedule
from app.main.model.user import User
from app.main.model.semester import Semester
from app.main.model.department import Department
from typing import Dict, Tuple
# 2023.1 09:00


class SchedulerService:
    @staticmethod
    def create_scheduler(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user, department_number = check_token(header)
            response_object, number = check_and_create_schedule(user,
                                                                department_number,
                                                                data)
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def read_scheduler(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user, department_number = check_token(header)
            response_object, number = read_database_function(user,
                                                             department_number,
                                                             data)
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def update_scheduler(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user, department_number = check_token(header)
            response_object, number = update_scheduler_function(user,
                                                                department_number,
                                                                data)
            return response_object, 200
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def delete_scheduler(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user, department_number = check_token(header)
            response_object, number = delete_function(user,
                                                      department_number,
                                                      data)
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def check_scheduler(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user, department_number = check_token(header)
            response_object, number = check_function(user,
                                                     department_number)
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number


# 토큰이 존재한다면 토큰이 유효한지 확인하고, 해당하는 부서 정보를 같이 리턴하는 함수
def check_token(header):
    now = find_semester_schedule()
    resp = User.decode_auth_token(header)
    user = User.query.filter(User.id == resp).first()
    if user.user_group == 1:
        department_number = 1
    else:
        department_number = Semester.query.filter(Semester.student_number == user.student_id,
                                                  Semester.working_semester_year.like('%' + now + '%')).first()
    return user, department_number


# 토큰이 존재하지 않으면 리턴하는 함수
def valid_token():
    response_object = {
        'status': 'fail',
        'message': 'Provide a valid auth token.'
    }
    return response_object, 401


# 실제 시간을 시간표로 변환하는 함수 (함수 인자가 list로 받아야 함)
def transform_database(start_time, end_time):
    if start_time[11] == '0':
        start_work_time = (int(start_time[8]) * 10 + int(start_time[9]) - 9) * 2 + 1
    else:
        start_work_time = (int(start_time[8]) * 10 + int(start_time[9]) - 9) * 2 + 2
    if end_time[11] == '0':
        end_work_time = (int(end_time[8]) * 10 + int(end_time[9]) - 9) * 2 + 1
    else:
        end_work_time = (int(end_time[8]) * 10 + int(end_time[9]) - 9) * 2 + 2
    return start_work_time, end_work_time


# int형태의 list를 string list로 변환, 즉 시간표를 실제 시간으로 변환
def transform_schedule(start_period_time, end_period_time):
    now = find_semester_schedule()
    start_work_time = now + " %d:%d" % (start_period_time / 2 + 9, (start_period_time % 2) * 30)
    end_work_time = now + " %d:%d" % (end_period_time / 2, (end_period_time % 2) * 30)
    return start_work_time, end_work_time


# schedule에 저장할 학기 정보 계산 함수
def find_semester_schedule():
    now = datetime.datetime.utcnow()
    if 2 < now.month < 9:
        return str(now.year) + ".1"
    else:
        return str(now.year) + ".2"


# 스케쥴 모델에 저장하는 함수
def save_new_schedule(data: Schedule) -> None:
    db.session.add(data)
    db.session.commit()


# 생성하기 전에 DB에 완전히 같은 데이터가 존재하는지 확인, 없다면 생성하여 저장 후 리턴
def check_and_create_schedule(user, department_number, data):
    if department_number == 1:
        department_number = Department.query.filter(
            Department.department_name == data['department_name']
        ).first()
    if data['work_start_time'] < 0 or data['work_start_time'] > 26 or data['work_end_time'] < 1 or data['work_end_time'] > 27:
        response_object = {
            'status': 'fail',
            'message': 'Provide wrong schedule.'
        }
        return response_object, 401
    else:
        work_start_time, work_end_time = transform_schedule(data['work_start_time'], data['work_end_time'])
        check = Schedule.query.filter(Schedule.student_number == user.student_id,
                                      Schedule.department_number == department_number.department_code,
                                      Schedule.day_of_week == data['work_of_day'],
                                      Schedule.work_start_time == data['work_start_time']).first()
        if check:
            response_object = {
                'status': 'fail',
                'message': 'The same schedule already exists'
            }
            return response_object, 401
        else:
            if user.group_id == 1 or user.group_id == 2:
                new_scheduler = Schedule(
                    student_number=data['student_id'],
                    department_number=department_number.department_code,
                    day_of_week=data['work_of_day'],
                    work_start_time=data['work_start_time'],
                    work_end_time=data['work_end_time']
                )
                save_new_schedule(new_scheduler)
            else:
                new_scheduler = Schedule(
                    student_number=user.student_id,
                    department_number=department_number.department_code,
                    day_of_week=data['work_of_day'],
                    work_start_time=data['work_start_time'],
                    work_end_time=data['work_end_time']
                )
                save_new_schedule(new_scheduler)
            response_object = {
                'status': 'success',
                'data': {
                    'department_number': department_number,
                    'student_number': user.student_id,
                    'day_of_week': new_scheduler.day_of_week,
                    'work_start_time': new_scheduler.work_start_time,
                    'work_end_time': new_scheduler.work_end_time
                }
            }
            return response_object, 200


# 시간표를 실제 시간으로 바꾼 후, 그 형태를 json형태로 변환 후 리턴
def read_database_function(user, department_number, data):
    work_start_time, work_end_time, work_of_days = list()
    now = find_semester_schedule()
    if department_number == 1:
        department_number = Department.query.filter(
            Department.department_name == data['department_name']
        ).first()

    if user.gruop_id == 0 or user.group_id == 1:  # user가 관리자인 경우
        scheduler_datas = Schedule.query.filter(Schedule.department_number == department_number.department_code,
                                                Schedule.work_start_time.like('%' + now + '%')).all()
        for scheduler_data in scheduler_datas:
            start_time, end_time = transform_database(scheduler_data.work_start_time,
                                                      scheduler_data.work_end_time)
            work_start_time.append(start_time)
            work_end_time.append(end_time)
            work_of_days.append(scheduler_data.day_of_week)
    else:  # user가 학생인 경우
        scheduler_datas = Schedule.query.filter(Schedule.student_number == user.student_id,
                                                Schedule.department_number == department_number.department_code,
                                                Schedule.work_start_time.like('%' + now + '%')).all()
        for scheduler_data in scheduler_datas:
            if scheduler_data.student_number == user.student_id:
                start_time, end_time = transform_database(scheduler_data.work_start_time,
                                                          scheduler_data.work_end_time)
                work_start_time.append(start_time)
                work_end_time.append(end_time)
                work_of_days.append(scheduler_data.day_of_week)
            else:
                continue
    response_object = {
        'status': 'success',
        'data': {
            'student_number': user.student_id,
            'department_number': department_number.department_code,
            'scheduler_datas': [
                {
                    'day_of_week': work_of_days[i],
                    'work_start_time': work_start_time[i],
                    'work_end_time': work_end_time[i]
                } for i in work_of_days.size()
            ]
        }
    }
    return response_object, 201


# 받은 데이터를 시간표로 변환 후 이 시간표가 DB에 존재하는지 확인, 있으면 update 진행, 안되면 fail 리턴
def update_scheduler_function(user, department_number, data):
    start_time = data['work_start_time']
    end_time = data['work_end_time']
    start_time, end_time = transform_schedule(start_time, end_time)
    if department_number == 1:
        department_number = Department.query.filter(
            Department.department_name == data['department_name']
        ).first()
    if user.gruop_id == 0 or user.group_id == 1:  # user가 관리자인 경우
        scheduler_data = Schedule.query.filter(Schedule.student_number == data['student_id'],
                                               Schedule.department_number == department_number.department_code,
                                               Schedule.day_of_week == data['day_of_week'],
                                               Schedule.work_start_time == start_time,
                                               Schedule.work_end_time == end_time).first()
    else:
        scheduler_data = Schedule.query.filter(Schedule.student_number == user.student_id,
                                               Schedule.department_number == department_number.department_code,
                                               Schedule.day_of_week == data['day_of_week'],
                                               Schedule.work_start_time == start_time,
                                               Schedule.work_end_time == end_time).first()
    update_start_time = data['update_work_start_time']
    update_end_time = data['update_work_start_time']
    update_start_time, update_end_time = transform_schedule(update_start_time, update_end_time)
    scheduler_data.work_start_time = update_start_time
    scheduler_data.work_end_time = update_end_time
    db.Schedule.commit()
    response_object = {
        'status': 'success',
        'data': {
            'student_number': user.student_id,
            'department_number': department_number.department_code,
            'day_of_week': scheduler_data.day_of_week,
            'work_start_time': update_start_time,
            'work_end_time': update_end_time
        }
    }
    return response_object, 200


# 해당하는 스케쥴이 존재하는지 확인한 후 존재한다면 삭제하는 함수
def delete_function(user, department_number, data):
    if user.user_group == 2:  # 요청한 자가 학생인 경우
        response_object = {
            'status': 'fail',
            'message': 'you are not the manager'
        }
        return response_object, 401
    start_time = data.get('work_start_time')
    end_time = data.get('work_end_time')
    start_time, end_time = transform_schedule(start_time, end_time)
    if user.gruop_id == 0 or user.group_id == 1:  # 관리자가 요청한 경우
        scheduler_data = Schedule.query.filter(Schedule.student_number == data['student_id'],
                                               Schedule.department_number == department_number.department_code,
                                               Schedule.day_of_week == data['day_of_week'],
                                               Schedule.work_start_time == start_time,
                                               Schedule.work_end_time == end_time).first()
    else:
        scheduler_data = Schedule.query.filter(Schedule.student_number == user.student_id,
                                               Schedule.department_number == department_number.department_code,
                                               Schedule.day_of_week == data['day_of_week'],
                                               Schedule.work_start_time == start_time,
                                               Schedule.work_end_time == end_time).first()
    if scheduler_data:
        response_object, number = delete_schedule(scheduler_data)
        return response_object, number
    else:
        response_object = {
            'status': 'fail',
            'message': 'This schedule does not exist in the database.'
        }
        return response_object, 402


# 스케줄 모델에 삭제하는 함수
def delete_schedule(data: Schedule):
    db.session.delete(data)
    db.session.commit()
    response_object = {
        'status': 'Delete success',
        'data': {
            'student_number': data.student_number,
            'department_number': data.department_number,
            'day_of_week': data.day_of_week,
            'work_start_time': data.work_start_time,
            'work_end_time': data.work_end_time
        }
    }
    return response_object, 200


def check_function(user, department_number):
    now = find_semester_schedule()
    if user.user_group == 2:  # 요청한 자가 학생인 경우
        response_object = {
            'status': 'fail',
            'message': 'you are not the manager'
        }
        return response_object, 401
    scheduler_datas = Schedule.query.filter(Schedule.department_number == department_number.department_code,
                                            Schedule.work_start_time.like('%' + now + '%')) \
        .order_by(Schedule.work_start_time) \
        .all()

    monday_list, tuesday_list, wednesday_list, thursday_list, friday_list = \
        count_scheduler(scheduler_datas)
    response_object, number = check_scheduler(monday_list,
                                              tuesday_list,
                                              wednesday_list,
                                              thursday_list,
                                              friday_list)
    return response_object, number


# 선택한 부서 및 해당 학기에 모든 스케쥴을 불러온 후, 월~금으로 나누어 시간표별로 저장하는 함수
def count_scheduler(scheduler_datas):
    monday_list = [0 for i in range(26)]
    tuesday_list = [0 for i in range(26)]
    wednesday_list = [0 for i in range(26)]
    thursday_list = [0 for i in range(26)]
    friday_list = [0 for i in range(26)]
    for scheduler_data in scheduler_datas:
        work_start_time, work_end_time = transform_database(scheduler_data.work_start_time,
                                                            scheduler_data.work_end_time)
        if scheduler_data.day_of_week == 'Monday':
            for i in range(work_start_time, work_end_time):
                monday_list[i] = monday_list[i] + 1
        elif scheduler_data.day_of_week == 'Tuesday':
            for i in range(work_start_time, work_end_time):
                tuesday_list[i] = tuesday_list[i] + 1
        elif scheduler_data.day_of_week == 'Wednesday':
            for i in range(work_start_time, work_end_time):
                wednesday_list[i] = wednesday_list[i] + 1
        elif scheduler_data.day_of_week == 'Thursday':
            for i in range(work_start_time, work_end_time):
                thursday_list[i] = thursday_list[i] + 1
        else:
            for i in range(work_start_time, work_end_time):
                friday_list[i] = friday_list[i] + 1
    return monday_list, tuesday_list, wednesday_list, thursday_list, friday_list


# 월~금까지 빈 시간이 있는지 확인하는 함수
def check_scheduler(monday_list, tuesday_list, wednesday_list, thursday_list, friday_list):
    for i in range(26):
        if (monday_list[i] == 0 or tuesday_list[i] == 0 or wednesday_list[i] == 0 or thursday_list[i] == 0 or
                friday_list[i] == 0):
            if monday_list[i] == 0:
                response_object = {
                    'status': 'fail',
                    'message': 'Monday period {} valid.'.format(i)
                }
                return response_object, 201
            elif tuesday_list[i] == 0:
                response_object = {
                    'status': 'fail',
                    'message': 'Tuesday period {} valid.'.format(i)
                }
                return response_object, 202
            elif wednesday_list[i] == 0:
                response_object = {
                    'status': 'fail',
                    'message': 'Wednesday period {} valid.'.format(i)
                }
                return response_object, 203
            elif thursday_list[i] == 0:
                response_object = {
                    'status': 'fail',
                    'message': 'Thursday period {} valid.'.format(i)
                }
                return response_object, 204
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Friday period {} valid.'.format(i)
                }
                return response_object, 205
        else:
            continue
    response_object = {
        'status': 'success',
        'message': 'Everyday is full'
    }
    return response_object, 200
