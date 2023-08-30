from flask_restx import Namespace, fields


class UserDto:
    api = Namespace("user", description="user related operations")
    user = api.model(
        "user",
        {
            "student_id": fields.String(required=True, description="user student id"),
            "username": fields.String(required=True, description="user username"),
            "password": fields.String(required=True, description="user password"),
        },
    )


class AuthDto:
    api = Namespace("auth", description="authentication related operations")
    user_auth = api.model(
        "auth_details",
        {
            "student_id": fields.String(required=True, description="The student id"),
            "password": fields.String(required=True, description="The user password "),
        },
    )


class AttendanceDto:
    api = Namespace("attendance", description="attendance related operations")
    user_attendance_read = api.model(
        "User Attendance read details",
        {
            "student_id": fields.String(required=False, description="read student id"),
            "department_name": fields.String(required=False, description="manager check department name")
        })
    user_work_start = api.model("User Attendance work start details", {})
    user_work_end = api.model("User Attendance work end details", {
        "work_text": fields.String(required=True, description="work context")
    })
    attendance_create = api.model(
        "Attendance update details",
        {
            "student_id": fields.String(required=True, description="manager use student id"),
            "department_name": fields.String(required=True, description="check department name"),
            "start_time": fields.String(required=True, description="student start time"),
            "end_time": fields.String(required=True, description="student end time"),
            "work_text": fields.String(required=True, description="student work context")
        })
    attendance_update = api.model(
        "Attendance update details",
        {
            "student_id": fields.String(required=True, description="manager use student id"),
            "department_name": fields.String(required=True, description="check department name"),
            "start_time": fields.String(required=True, description="user start time"),
            "update_end_time": fields.String(required=True, description="user update start time"),
        })
    attendance_delete = api.model(
        "Attendance delete details",
        {
            "student_id": fields.String(required=False, description="manager required student id"),
            "start_time": fields.String(required=True, description="student start time"),
            "end_time": fields.String(required=True, description="student end time"),
            "department_name": fields.String(required=False, description="top manager required department name")
        })


class UserPageDto:
    api = Namespace("User_page", description="User page related operations")
    user_page = api.model(
        "user_page_details",
        {
            "": fields.String(),
        },
    )


class UserSchedulerDto:
    api = Namespace("User_Scheduler", description="User Scheduler related operations")
    user_scheduler_read = api.model(
        "Read Scheduler",
        {"department_name": fields.String(required=False, description="check department name")})
    user_scheduler_create = api.model(
        "User Scheduler create details",
        {
            "work_start_time": fields.String(required=True, description="user start time"),
            "work_end_time": fields.String(required=True, description="user end time"),
            "work_of_day": fields.String(required=True, description="user working day"),
        },
    )
    user_scheduler_update = api.model(
        "User Scheduler update details",
        {
            "work_start_time": fields.String(required=True, description="user start time"),
            "work_end_time": fields.String(required=True, description="user end time"),
            "work_of_day": fields.String(required=True, description="user working day"),
            "update_work_start_time": fields.String(required=True, description="user update start time"),
            "update_work_end_time": fields.String(required=True, description="user update end time")
        })
    user_scheduler_delete = api.model(
        "User Scheduler delete details",
        {
            "work_start_time": fields.String(required=True, description="user start time"),
            "work_end_time": fields.String(required=True, description="user end time"),
            "work_of_day": fields.String(required=True, description="user working day"),
        })
    user_scheduler_check = api.model(
        "Manager check Scheduler",
        {
            "department_name": fields.String(required=True, description="check department name")
        })


class AnnouncementDto:
    api = Namespace("announcement", description="Announcement related operations")
    create_announcement = api.model(
        "Create Announcement",
        {
            "department_number": fields.String(
                required=True, description="The department number of the author"
            ),
            "student_number": fields.String(
                required=True, description="The student number of the author"
            ),
            "announcement_title": fields.String(
                required=True, description="The title of the announcement"
            ),
            "announcement_text": fields.String(
                required=True, description="The text content of the announcement"
            ),
        },
    )
    read_announcements = api.model(
        "Read Announcements",
        {},
    )
    read_announcement = api.model(
        "Read Announcement",
        {
            "announcement_key": fields.Integer(
                required=True, description="The key of the announcement to delete"
            )
        },
    )

    update_announcement = api.model(
        "Update Announcement",
        {
            "department_number": fields.String(
                required=True,
                description="The updating department number of the author",
            ),
            "student_number": fields.String(
                required=True, description="The updating student number of the author"
            ),
            "announcement_title": fields.String(
                required=True, description="The updating title of the announcement"
            ),
            "announcement_text": fields.String(
                required=True,
                description="The updating text content of the announcement",
            ),
        },
    )
    delete_announcement = api.model(
        "Delete Announcement",
        {
            "announcement_key": fields.Integer(
                required=True, description="The key of the announcement to delete"
            )
        },
    )


class DepartmentDto:
    api = Namespace('Department', description='Manage Department')
    department_create = api.model('Manager read Scheduler', {
        'department_name': fields.String(required=True, description='check department name'),
        'department_code': fields.String(required=True, description='check department code'),
        'number_of_working_students': fields.String(required=True, description='check number of working students')
    })
    department_join = api.model('User join Department', {
        'student_id': fields.String(required=True, description='Student Number to join department'),
        'department_name': fields.String(required=False, description='Student join department name'),
    })
    department_update = api.model('Manager control Department Semester', {
        'department_name': fields.String(required=True, description='check department name'),
        'number_of_working_students': fields.String(required=True, description='modify semester')
    })


class UserGroupDto:
    api = Namespace('user_group', description='User Group Manage')
    user_group_create = api.model('User Group Create', {
        'user_group_name': fields.String(required=True, description='Create Group Name'),
        'authority_context': fields.String(required=True, description='Create Group authority context')
    })
    user_group_update = api.model('User Group Update', {
        'user_group_name': fields.String(required=True, description='Create Group Name'),
        'authority_context': fields.String(required=False, description='Create Group authority context'),
        'update_user_group_name': fields.String(required=False, description='Create Group authority context'),
        'update_user_group_code': fields.String(required=False, description='Create Group authority context'),
        'update_group_authority': fields.String(required=False, description='Create Group authority context'),

    })
    user_group_join = api.model('User Join Group', {
        'student_number': fields.String(required=True, description=''),
        'user_group_name': fields.String(required=True, description='')
    })
