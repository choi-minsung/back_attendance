from flask import request
from flask_restx import Resource
from app.main.service.user_group_service import UserGroupService
from ..util.dto import UserGroupDto
from typing import Dict, Tuple

api = UserGroupDto.api
create_user_group = UserGroupDto.user_group_create
update_user_group = UserGroupDto.user_group_update
join_user_group = UserGroupDto.user_group_join


@api.route('/create_department')
class CreateDepartment(Resource):
    """
        Manager Create Department
    """
    @api.expect(create_user_group, validate=True)
    @api.response(201, 'Success Manager Create Department')
    @api.doc('Manager Create Department')
    def post(self) -> Tuple[Dict[str, str], int]:
        """ Read Attendance in my department """
        auth_header = request.headers.get('Authorization')
        data = request.json
        return UserGroupService.create_user_group(header=auth_header, data=data)


@api.route('/update_department')
class UpdateDepartment(Resource):
    """
        Manager Update Department
    """
    @api.expect(update_user_group, validate=True)
    @api.response(201, 'Success Manager Update Department')
    @api.doc('Manager Update Department')
    def patch(self) -> Tuple[Dict[str, str], int]:
        """ Read Attendance in my department """
        auth_header = request.headers.get('Authorization')
        data = request.json
        return UserGroupService.update_user_group(header=auth_header, data=data)


@api.route('/join_department')
class JoinDepartment(Resource):
    """
        Student Join Department
    """
    @api.expect(join_user_group, validate=True)
    @api.response(201, 'Success Student Join Department')
    @api.doc('Student Join Department')
    def patch(self) -> Tuple[Dict[str, str], int]:
        """ Read Attendance in my department """
        auth_header = request.headers.get('Authorization')
        data = request.json
        return UserGroupService.join_user_group(header=auth_header, data=data)
