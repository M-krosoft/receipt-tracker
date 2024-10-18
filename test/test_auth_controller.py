import unittest
from unittest.mock import patch

from faker import Faker

from app import create_app, db
from app.app_config import TestingConfig
from app.models.user import User
from app.requests import RegisterRequest, LoginRequest
from test.models_factory import ModelsFactory

fake = Faker()


class TestAuthController(unittest.TestCase):

    def setUp(self):
        self.config = TestingConfig()
        self.app = create_app(config=self.config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_should_be_success(self):
        # given
        register_request = RegisterRequest(name=fake.name(), email=fake.email(), password=fake.password())

        # when
        response = self.client.post("/receipt-tracker/auth/register", json=register_request.__dict__)

        # then
        saved_user = User.query.filter_by(email=register_request.email).first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.name, register_request.name)
        self.assertEqual(saved_user.email, register_request.email)
        self.assertNotEqual(saved_user.password, register_request.password)
        self.assertIsNotNone(saved_user.created_date)
        self.assertIsNotNone(saved_user.id)

    def test_register_should_return_email_taken_error(self):
        # given
        saved_user = ModelsFactory.create_user_in_db()
        register_request = RegisterRequest(name=fake.name(), email=saved_user.email, password=fake.password())

        # when
        response = self.client.post("/receipt-tracker/auth/register", json=register_request.__dict__)

        # then
        response_json = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json["error"], "EmailTakenError")
        self.assertIsNotNone(response_json["message"])

    def test_register_should_return_invalid_request_error(self):
        # given
        register_request = RegisterRequest()

        # when
        response = self.client.post("/receipt-tracker/auth/register", json=register_request.__dict__)

        # then
        response_json = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json["error"], "InvalidRequestFieldError")
        self.assertIsNotNone(response_json["message"])

    @patch('app.services.auth_service.check_password_hash')
    def test_login_should_be_success(self, mock_check_password_hash):
        # given
        password = "<PASSWORD>"
        saved_user = ModelsFactory.create_user_in_db(password=password)
        login_request = LoginRequest(email=saved_user.email, password=password)
        mock_check_password_hash.return_value = True

        # when
        response = self.client.post("/receipt-tracker/auth/login", json=login_request.__dict__)

        # then
        response_json = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response_json["accessToken"])

    def test_login_should_return_user_not_exist_error(self):
        # given
        login_request = LoginRequest(email=fake.email(), password=fake.password())

        # when
        response = self.client.post("/receipt-tracker/auth/login", json=login_request.__dict__)

        # then
        response_json = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json["error"], "UserNotExistError")
        self.assertIsNotNone(response_json["message"])

    def test_login_should_return_invalid_password_error(self):
        # given
        saved_user = ModelsFactory.create_user_in_db()
        wrong_password = saved_user.password + fake.password()
        login_request = LoginRequest(email=saved_user.email, password=wrong_password)

        # when
        response = self.client.post("/receipt-tracker/auth/login", json=login_request.__dict__)

        # then
        response_json = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json["error"], "InvalidPasswordError")
        self.assertIsNotNone(response_json["message"])
