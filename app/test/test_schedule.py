import unittest

from app.main import db
import json
from app.test.base import BaseTestCase
from app.test.test_auth import register_user, register_integration_manager, register_department_manager, \
    login_integration_manager, login_department_manager, login_user


def user(self):
    register_user(self)
    return login_user(self)


def integration_manager(self):
    register_integration_manager(self)
    return login_integration_manager(self)


def department_manager(self):
    register_department_manager(self)
    return login_department_manager(self)


class TestScheduleBlueprint(BaseTestCase):
    def test_schedule_user_check(self):
        """ Test for user registration """
        with self.client:
            user_login = user(self)
            data = json.loads(user_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(user_login.content_type == 'application/json')
            self.assertEqual(user_login.status_code, 201)
            response = self.client.post(
                '/User_Scheduler/check_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        user_login.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'you are not the manager')
            self.assertEqual(response.status_code, 200)

    def test_schedule_department_manager_check(self):
        """ Test for user registration """
        with self.client:
            department_login = department_manager(self)
            data = json.loads(department_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(department_login.content_type == 'application/json')
            self.assertEqual(department_login.status_code, 201)
            response = self.client.post(
                '/User_Scheduler/check_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        department_login.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Everyday is full')
            self.assertEqual(response.status_code, 200)

    def test_schedule_integration_manager_check(self):
        """ Test for user registration """
        with self.client:
            integration_login = integration_manager(self)
            data = json.loads(integration_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(integration_login.content_type == 'application/json')
            self.assertEqual(integration_login.status_code, 201)
            response = self.client.post(
                '/User_Scheduler/check_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        integration_login.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Everyday is full')
            self.assertEqual(response.status_code, 200)

    def test_schedule_user_read(self):
        """ Test registration with already registered email"""
        with self.client:
            user_login = user(self)
            data = json.loads(user_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(user_login.content_type == 'application/json')
            self.assertEqual(user_login.status_code, 201)
            response = self.client.post(
                '/User_Scheduler/read_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        user_login.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_schedule_department_manager_read(self):
        """ Test registration with already registered email"""
        with self.client:
            department_manager_login = department_manager(self)
            data = json.loads(department_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(department_manager_login.content_type == 'application/json')
            self.assertEqual(department_manager_login.status_code, 201)
            response = self.client.post(
                '/User_Scheduler/read_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        department_manager_login.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_schedule_integration_manager_read(self):
        """ Test registration with already registered email"""
        with self.client:
            integration_manager_login = integration_manager(self)
            data = json.loads(integration_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(integration_manager_login.content_type == 'application/json')
            self.assertEqual(integration_manager_login.status_code, 201)
            response = self.client.post(
                '/User_Scheduler/read_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        integration_manager_login.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_schedule_department_manager_update(self):
        """ Test for login of registered-user login """
        with self.client:
            department_manager_login = department_manager(self)
            data = json.loads(department_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(department_manager_login.content_type == 'application/json')
            self.assertEqual(department_manager_login.status_code, 201)
            response = self.client.post(
                '/User_Scheduler/update_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        department_manager_login.data.decode()
                    )['Authorization']
                ),
                data=json.dumps(dict(
                    student_id='',
                    day_of_week='194909111',
                    work_start_time='',
                    work_end_time='',
                    update_work_start_time='',
                    update_work_end_time=''
                ))
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_schedule_integration_manager_update(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            integration_manager_login = integration_manager(self)
            data = json.loads(integration_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(integration_manager_login.content_type == 'application/json')
            self.assertEqual(integration_manager_login.status_code, 201)
            # registered user login
            response = self.client.post(
                '/User_Scheduler/update_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        integration_manager_login.data.decode()
                    )['Authorization']
                ),
                data=json.dumps(dict(
                    student_id='',
                    day_of_week='194909111',
                    work_start_time='',
                    work_end_time='',
                    update_work_start_time='',
                    update_work_end_time=''
                ))
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_schedule_department_manager_delete(self):
        """ Test for login of non-registered user """
        with self.client:
            user = login_user(self)
            data = json.loads(user.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(user.content_type == 'application/json')
            self.assertEqual(user.status_code, 201)
            response = self.client.post(
                '/User_Scheduler/update_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        user.data.decode()
                    )['Authorization']
                ),
                data=json.dumps(dict(
                    day_of_week='194909111',
                    work_start_time='',
                    work_end_time=''
                ))
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_schedule_integration_manager_delete(self):
        """ Test for login of non-registered user """
        with self.client:
            integration_manager_login = integration_manager(self)
            data = json.loads(integration_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(integration_manager_login.content_type == 'application/json')
            self.assertEqual(integration_manager_login.status_code, 201)
            response = self.client.post(
                '/User_Scheduler/update_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        integration_manager_login.data.decode()
                    )['Authorization']
                ),
                data=json.dumps(dict(
                    student_id='',
                    day_of_week='194909111',
                    work_start_time='',
                    work_end_time=''
                ))
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_schedule_user_create(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            user_login = user(self)
            data = json.loads(user_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(user_login.content_type == 'application/json')
            self.assertEqual(user_login.status_code, 201)
            # user login
            response = self.client.post(
                '/User_Scheduler/update_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        user_login.data.decode()
                    )['Authorization']
                ),
                data=json.dumps(dict(
                    day_of_week='194909111',
                    work_start_time='',
                    work_end_time=''
                ))
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_schedule_department_manager_create(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            department_manager_login = department_manager(self)
            data = json.loads(department_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(department_manager_login.content_type == 'application/json')
            self.assertEqual(department_manager_login.status_code, 201)
            # user login
            response = self.client.post(
                '/User_Scheduler/update_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        department_manager_login.data.decode()
                    )['Authorization']
                ),
                data=json.dumps(dict(
                    day_of_week='194909111',
                    work_start_time='',
                    work_end_time=''
                ))
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_schedule_integration_manager_create(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            integration_manager_login = integration_manager(self)
            data = json.loads(integration_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(integration_manager_login.content_type == 'application/json')
            self.assertEqual(integration_manager_login.status_code, 201)
            # user login
            response = self.client.post(
                '/User_Scheduler/update_scheduler',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        integration_manager_login.data.decode()
                    )['Authorization']
                ),
                data=json.dumps(dict(
                    day_of_week='194909111',
                    work_start_time='',
                    work_end_time=''
                ))
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
