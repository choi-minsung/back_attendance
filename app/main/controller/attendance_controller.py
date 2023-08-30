from flask import request
from flask_restx import Resource
from app.main.service.attendance_service import Attendance
from ..util.dto import AttendanceDto
from typing import Dict, Tuple

api = AttendanceDto.api
user_attendance_read = AttendanceDto.user_attendance_read
user_work_start = AttendanceDto.user_work_start
user_work_end = AttendanceDto.user_work_end
attendance_create = AttendanceDto.attendance_create
attendance_update = AttendanceDto.attendance_update
attendance_delete = AttendanceDto.attendance_delete


@api.route("/read_attendance")
class UserReadAttendance(Resource):
    """
    User Read Attendance Resource
    """

    @api.expect(user_attendance_read, validate=False)
    @api.response(201, "User read attendance in semester")
    @api.doc("User read attendance in semester")
    def get(self) -> Tuple[Dict[str, str], int]:
        """Read Attendance in my department"""
        auth_header = request.headers.get("Authorization")
        data = request.json
        return Attendance.read_attendance(header=auth_header, data=data)


@api.route("/start_attendance")
class UserWorkStart(Resource):
    """
    User Start Work Resource
    """

    @api.expect(user_work_start, validate=False)
    @api.response(201, "User work start attendance in semester")
    @api.doc("user start work in semester")
    def post(self):
        # get auth token
        auth_header = request.headers.get("Authorization")
        return Attendance.work_start(header=auth_header)


@api.route("/end_attendance")
class UserWorkEnd(Resource):
    """
    User End Work Resource
    """

    @api.expect(user_work_end, validate=True)
    @api.response(201, "User work end attendance in semester")
    @api.doc("user leave work in semester")
    def patch(self):
        auth_header = request.headers.get("Authorization")
        data = request.json
        return Attendance.leave_work(header=auth_header, data=data)


@api.route("/create_attendance")
class CreateAttendance(Resource):
    """
    Manager Create Attendance Resource
    """

    @api.expect(attendance_create, validate=True)
    @api.response(201, "Create attendance in semester")
    @api.doc("manager create attendance in semester")
    def post(self):
        auth_header = request.headers.get("Authorization")
        data = request.json
        return Attendance.create_attendance(header=auth_header, data=data)


@api.route("/delete_attendance")
class DeleteAttendance(Resource):
    """
    Admin Delete Attendance Resource
    """

    @api.expect(attendance_delete, validate=True)
    @api.response(201, "Delete attendance in semester")
    @api.doc("admin delete attendance in semester")
    def delete(self):
        auth_header = request.headers.get("Authorization")
        data = request.json
        return Attendance.delete_attendance(header=auth_header, data=data)


@api.route("/update_attendance")
class UpdateAttendance(Resource):
    """
    Admin Update Attendance
    """

    @api.expect(attendance_update, validate=True)
    @api.response(201, "User update attendance in semester")
    @api.doc("admin update attendance in semester")
    def patch(self):
        auth_header = request.headers.get("Authorization")
        data = request.json
        return Attendance.update_attendance(header=auth_header, data=data)
