from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.attendance_controller import api as attendance_ns
from .main.controller.user_page_controller import api as user_page_ns
from .main.controller.scheduler_controller import api as scheduler_ns
from .main.controller.announcement_controller import api as announcement_ns
from .main.controller.department_controller import api as department_ns
from .main.controller.user_group_controller import api as user_group_ns

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='FLASK RESTPLUS(RESTX) API BOILER-PLATE WITH JWT',
    version='1.0',
    description='a boilerplate for flask restplus (restx) web service',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(attendance_ns)
api.add_namespace(user_page_ns)
api.add_namespace(scheduler_ns)
api.add_namespace(announcement_ns)
api.add_namespace(department_ns)
api.add_namespace(user_group_ns)
