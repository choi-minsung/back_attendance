from flask import request
from flask_restx import Resource
from app.main.service.scheduler_service import SchedulerService
from app.main.service.auth_helper import Auth
from ..util.dto import UserSchedulerDto
from typing import Dict, Tuple

api = UserSchedulerDto.api
user_scheduler_read = UserSchedulerDto.user_scheduler_read
user_scheduler_create = UserSchedulerDto.user_scheduler_create
user_scheduler_check = UserSchedulerDto.user_scheduler_check
user_scheduler_delete = UserSchedulerDto.user_scheduler_delete
user_scheduler_update = UserSchedulerDto.user_scheduler_update


@api.route('/read_scheduler')
class UserReadScheduler(Resource):
    """
        User Read Scheduler Resource
    """

    @api.expect(user_scheduler_read, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user scheduler')
    def get(self) -> Tuple[Dict[str, str], int]:
        """ Read Scheduler in my department """
        auth_header = request.headers.get("Authorization")
        data = request.json
        return SchedulerService.read_scheduler(header=auth_header, data=data)


@api.route('/create_scheduler')
class UserCreateScheduler(Resource):
    """
        User Create Scheduler Resource
    """
    @api.expect(user_scheduler_create, validate=True)
    @api.doc('user create scheduler in semester')
    def post(self):
        # get auth token
        auth_header = request.headers.get("Authorization")
        data = request.json
        return SchedulerService.create_scheduler(header=auth_header, data=data)


@api.route('/update_scheduler')
class UserUpdateScheduler(Resource):
    """
        User Update Scheduler Resource
    """

    @api.expect(user_scheduler_update, validate=True)
    @api.doc('user update scheduler in semester')
    def patch(self):
        auth_header = request.headers.get("Authorization")
        data = request.json
        return SchedulerService.update_scheduler(header=auth_header, data=data)


@api.route('/delete_scheduler')
class UserDeleteScheduler(Resource):
    """
        User Delete Scheduler Resource
    """

    @api.expect(user_scheduler_delete, validate=True)
    @api.doc('user delete scheduler in semester')
    def delete(self):
        auth_header = request.headers.get("Authorization")
        data = request.json
        return SchedulerService.delete_scheduler(header=auth_header, data=data)


@api.route('/check_scheduler')
class CheckScheduler(Resource):
    """
        Admin Check Scheduler
    """

    @api.expect(user_scheduler_check, validate=True)
    @api.doc('admin check scheduler in semester')
    def get(self):
        auth_header = request.headers.get("Authorization")
        data = request.json
        return SchedulerService.check_scheduler(header=auth_header, data=data)
