from app.main import db
from app.main.model.user_group import User_group
from app.main.model.authority import Authority
from app.main.model.user import User
from typing import Dict, Tuple
from app.main.service.scheduler_service import valid_token
from app.main.service.department_service import check_user


class UserGroupService:
    @staticmethod
    def create_user_group(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user = check_user(header)
            if user.user_group == 1:
                response_object, number = create_user_group_function(data)
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Access is not possible because you are not a full administrator.'
                }
                number = 401
            return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def join_user_group(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user = check_user(header)
            if user.user_group == 3:
                response_object = {
                    'status': 'fail',
                    'message': 'Access is not possible because you are not a full administrator.'
                }
                number = 401
                return response_object, number
            else:
                response_object, number = join_user_group_function(data)
                return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number

    @staticmethod
    def update_user_group(header: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        if header:
            user = check_user(header)
            if user.user_group == 3:
                response_object = {
                    'status': 'fail',
                    'message': 'Access is not possible because you are not a full administrator.'
                }
                number = 401
                return response_object, number
            else:
                response_object, number = update_user_group_function(data)
                return response_object, number
        else:
            response_object, number = valid_token()
            return response_object, number


def save_user_group_changes(data: User_group) -> None:
    db.session.add(data)
    db.session.commit()


def save_authority_changes(data: Authority) -> None:
    db.session.add(data)
    db.session.commit()


def create_user_group_function(data):
    authority = Authority.query.filter(
        Authority.authority_context == data["authority_context"]).first()
    if authority:
        new_user_group = User_group(
            user_group_name=data["user_group_name"],
            group_authority=authority.authority_key
        )
        save_user_group_changes(new_user_group)
    else:
        new_authority = Authority(
            authority_context=data["authority_context"]
        )
        save_authority_changes(new_authority)
        new_user_group = User_group(
            user_group_name=data["user_group_name"],
            group_authority=new_authority.authority_key
        )
        save_user_group_changes(new_user_group)
    response_object = {
        'status': 'success',
        'department number': new_user_group.user_group_name
    }
    return response_object, 200


def update_user_group_function(data):
    user_group = User_group.query.filter(
        User_group.user_group_name == data["user_group_name"],
    ).first()
    if user_group:
        if data["update_user_group_name"]:
            user_group.user_group_name = data["update_user_group_name"]
            user_group.user_group_code = data["update_user_group_code"]
            db.session.commit()
        elif data["update_user_group_code"]:
            user_group.user_group_code = data["update_user_group_code"]
            db.session.commit()
        elif data["update_group_authority"]:
            authority = Authority.query.filter(
                Authority.authority_context == data["update_group_authority"],
            )
            authority.authority_context = data["update_authority_context"]
            db.session.commit()
    else:
        response_object = {
            'status': 'fail',
            'message': 'Not Matched User Group Name'
        }
        return response_object, 200


def join_user_group_function(data):
    user_group = User_group.query.filter(
        User_group.user_group_name == data["user_group_name"],
    ).first()
    if user_group:
        user = User.query.filter(
            User.student_id == data["student_number"]
        ).first()
        user.user_group = user_group.user_group_key
        db.session.commit()
        response = {
            'status': 'success',
            'data': {
                'joined user': user.student_id,
                'joined user group': user.user_group
            }
        }
        return response, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Not Matched User Group Name'
        }
        return response_object, 200
