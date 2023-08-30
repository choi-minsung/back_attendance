from flask import request
from flask_restx import Resource
from app.main.service.department_service import DepartmentService
from ..util.dto import DepartmentDto
from typing import Dict, Tuple

api = DepartmentDto.api
create_department = DepartmentDto.department_create
update_department = DepartmentDto.department_update
join_department = DepartmentDto.department_join


@api.route('/create_department')
class CreateDepartment(Resource):
    """
        Manager Create Department
    """
    @api.expect(create_department, validate=True)
    @api.response(201, 'Success Manager Create Department')
    @api.doc('Manager Create Department')
    def post(self) -> Tuple[Dict[str, str], int]:
        """ Read Attendance in my department """
        auth_header = request.headers.get('Authorization')
        data = request.json
        return DepartmentService.create_department(header=auth_header, data=data)


@api.route('/update_department')
class UpdateDepartment(Resource):
    """
        Manager Update Department
    """
    @api.expect(update_department, validate=True)
    @api.response(201, 'Success Manager Update Department')
    @api.doc('Manager Update Department')
    def patch(self) -> Tuple[Dict[str, str], int]:
        """ Read Attendance in my department """
        auth_header = request.headers.get('Authorization')
        data = request.json
        return DepartmentService.update_department(header=auth_header, data=data)


@api.route('/join_department')
class JoinDepartment(Resource):
    """
        Student Join Department
    """
    @api.expect(join_department, validate=True)
    @api.response(201, 'Success Student Join Department')
    @api.doc('Student Join Department')
    def post(self) -> Tuple[Dict[str, str], int]:
        """ Read Attendance in my department """
        auth_header = request.headers.get('Authorization')
        data = request.json
        return DepartmentService.join_department(header=auth_header, data=data)
