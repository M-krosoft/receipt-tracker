import unittest
from unittest import mock
from unittest.mock import patch

from app.dtos.user_dto import UserDTO
from app.exceptions import EmailTakenError, UserNameEmptyError, InvalidPasswordError
from app.repositories.user_repository import UserRepository
from app.requests import RegisterRequest, LoginRequest
from app.services.auth_service import AuthService


def _create_user_dto(email, name) -> UserDTO:
    user_dto = UserDTO()
    user_dto.email = email
    user_dto.name = name
    user_dto.password = '<PASSWORD>'
    return user_dto


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = mock.Mock(spec=UserRepository)
        self.sut = AuthService(self.mock_repository)

    @patch('app.services.auth_service.generate_password_hash')
    def test_register_user_should_succeed(self, mock_generate_password_hash):
        # given
        register_request = RegisterRequest(name="<NAME>", email="<EMAIL>", password="<PASSWORD>")
        self.mock_repository.does_user_exist.return_value = False

        # when
        self.sut.register_user(register_request)

        # then
        self.mock_repository.does_user_exist.assert_called_once_with(register_request.email)
        self.mock_repository.create_new_user.assert_called_once_with(unittest.mock.ANY)
        mock_generate_password_hash.assert_called_once_with(register_request.password)

    def test_register_user_should_throw_email_taken_error(self):
        # given
        register_request = RegisterRequest(name="<NAME>", email="<EMAIL>", password="<PASSWORD>")
        self.mock_repository.does_user_exist.return_value = True

        # when && then
        with self.assertRaises(EmailTakenError):
            self.sut.register_user(register_request)
            self.mock_repository.does_user_exist.assert_called_once_with(register_request.email)

    def test_register_user_should_throw_empty_name_error(self):
        # given
        register_request = RegisterRequest(name=None, email="<EMAIL>", password="<PASSWORD>")
        self.mock_repository.does_user_exist.return_value = False

        # when && then
        with self.assertRaises(UserNameEmptyError):
            self.sut.register_user(register_request)
            self.mock_repository.does_user_exist.assert_called_once_with(register_request.email)

    @patch('app.services.auth_service.check_password_hash')
    @patch('app.services.auth_service.create_access_token')
    def test_authenticate_user_should_succeed(self, mock_create_access_token, mock_check_password_hash):
        # given
        login_request = LoginRequest(email="<EMAIL>", password=" < PASSWORD > ")
        token = 'token'

        mock_check_password_hash.return_value = True
        mock_create_access_token.return_value = token

        user = UserDTO(id=1, name="name", email=login_request.email, password=login_request.password)
        self.mock_repository.get_user_by_email.return_value = user

        # when
        access_token = self.sut.authenticate(login_request)

        # then
        self.mock_repository.get_user_by_email.assert_called_once_with(login_request.email)
        self.assertEqual(access_token, token)

    @patch('app.services.auth_service.check_password_hash')
    def test_authenticate_user_should_throw_invalid_password_error(self, mock_check_password_hash):
        # given
        login_request = LoginRequest(email="<EMAIL>", password=" < PASSWORD > ")
        mock_check_password_hash.return_value = False

        user = UserDTO(id=1, name="name", email=login_request.email, password=login_request.password)
        self.mock_repository.get_user_by_email.return_value = user

        # when && then
        with self.assertRaises(InvalidPasswordError):
            self.sut.authenticate(login_request)
