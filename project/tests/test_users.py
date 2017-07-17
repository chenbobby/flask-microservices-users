# project/tests/test_users.py

import json

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User


def add_test_user(username='test', email='test@example.com'):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """
    Tests for User Service
    """

    def test_users(self):
        """Ensure /ping route sends proper response"""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure POST /users properly adds user to database"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='test',
                    email='test@example.com'
                )),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('test@example.com added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure POST /users with invalid JSON throws error"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid POST Payload', data['message'])
            self.assertIn('failure', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Ensure POST /users with invalid JSON keys throws error"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    name='bob',
                    address='123 Main St.'
                    )),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid JSON Keys', data['message'])
            self.assertIn('failure', data['status'])

    def test_add_user_duplicate_user(self):
        """Ensure POST /users with existing email throws error"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='test1',
                    email='test@example.com'
                    )),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='test2',
                    email='test@example.com'
                    )),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Email already in use', data['message'])
            self.assertIn('failure', data['status'])

    def test_get_single_user(self):
        """Ensure GET /users/user_id returns valid response"""
        user = add_test_user()

        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('test', data['data']['username'])
            self.assertIn('test@example.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_get_single_user_invalid_id(self):
        """Ensure GET /users/(non-Int) throws error"""
        with self.client:
            response = self.client.get('/users/foobar')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('failure', data['status'])

    def test_get_single_user_nonexistent_id(self):
        """Ensure GET /users/id_out_of_range throws error"""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('failure', data['status'])

    def test_get_all_users(self):
        """Ensure GET /users returns all user details"""
        user1 = add_test_user('test1', 'test1@example.com')
        user2 = add_test_user('test2', 'test2@example.com')

        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('created_at', data['data']['users'][0])
            self.assertIn('created_at', data['data']['users'][1])
            self.assertIn('test1',
                        data['data']['users'][0]['username'])
            self.assertIn('test1@example.com',
                        data['data']['users'][0]['email'])
            self.assertIn('test2',
                        data['data']['users'][1]['username'])
            self.assertIn('test2@example.com',
                        data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Ensure main route behaves when no users in database"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """Ensure main route gets users from database"""
        user1 = add_test_user('test1', 'test1@example.com')
        user2 = add_test_user('test2', 'test2@example.com')

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertNotIn(b'<p>No users!</p>', response.data)
        self.assertIn(b'<strong>test1</strong>', response.data)
        self.assertIn(b'<strong>test2</strong>', response.data)

    def test_main_add_user(self):
        """Ensure main route can save user to database"""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='test1', email='test@example.com'),
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'<strong>test1</strong>', response.data)
