import unittest

from app.main import db
import json
from app.test.base import BaseTestCase
from app.test.test_schedule import user, integration_manager, department_manager


class TestAttendanceBlueprint(BaseTestCase):
    def test_attendance_user_start(self):
        """ Test for user registration """
        with self.client:
            user_login = user(self)
            data = json.loads(user_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(user_login.content_type == 'application/json')
            self.assertEqual(user_login.status_code, 201)
            response = self.client.post(
                '/attendance/start_attendance',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        user_login.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

    def test_attendance_department_manager_create(self):
        """ Test for user registration """
        with self.client:
            department_manager_login = department_manager(self)
            data = json.loads(department_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(department_manager_login.content_type == 'application/json')
            self.assertEqual(department_manager_login.status_code, 201)

    def test_attendance_integration_manager_create(self):
        """ Test for user registration """
        with self.client:
            integration_manager_login = integration_manager(self)
            data = json.loads(integration_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(integration_manager_login.content_type == 'application/json')
            self.assertEqual(integration_manager_login.status_code, 201)

    def test_attendance_user_end(self):
        """ Test registration with already registered email"""
        with self.client:
            user_login = user(self)
            data = json.loads(user_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(user_login.content_type == 'application/json')
            self.assertEqual(user_login.status_code, 201)
            response = self.client.post(
                '/attendance/end_attendance',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        user_login.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

    def test_attendance_department_manager_update(self):
        """ Test registration with already registered email"""
        with self.client:
            department_manager_login = department_manager(self)
            data = json.loads(department_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(department_manager_login.content_type == 'application/json')
            self.assertEqual(department_manager_login.status_code, 201)

    def test_attendance_integration_manager_update(self):
        """ Test registration with already registered email"""
        with self.client:
            integration_manager_login = integration_manager(self)
            data = json.loads(integration_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(integration_manager_login.content_type == 'application/json')
            self.assertEqual(integration_manager_login.status_code, 201)

    def test_attendance_department_manager_delete(self):
        """ Test for login of non-registered user """
        with self.client:
            department_manager_login = department_manager(self)
            data = json.loads(department_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(department_manager_login.content_type == 'application/json')
            self.assertEqual(department_manager_login.status_code, 201)

    def test_attendance_integration_manager_delete(self):
        """ Test for login of non-registered user """
        with self.client:
            integration_manager_login = integration_manager(self)
            data = json.loads(integration_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(integration_manager_login.content_type == 'application/json')
            self.assertEqual(integration_manager_login.status_code, 201)

    def test_attendance_user_read(self):
        """ Test for logout before token expires """
        with self.client:
            user_login = user(self)
            data = json.loads(user_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(user_login.content_type == 'application/json')
            self.assertEqual(user_login.status_code, 201)
            response = self.client.post(
                '/attendance/start_attendance',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        user_login.data.decode()
                    )['Authorization']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

    def test_attendance_department_manager_read(self):
        """ Test for logout before token expires """
        with self.client:
            department_manager_login = department_manager(self)
            data = json.loads(department_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(department_manager_login.content_type == 'application/json')
            self.assertEqual(department_manager_login.status_code, 201)

    def test_attendance_integration_manager_read(self):
        """ Test for logout before token expires """
        with self.client:
            integration_manager_login = integration_manager(self)
            data = json.loads(integration_manager_login.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(integration_manager_login.content_type == 'application/json')
            self.assertEqual(integration_manager_login.status_code, 201)


if __name__ == '__main__':
    unittest.main()
