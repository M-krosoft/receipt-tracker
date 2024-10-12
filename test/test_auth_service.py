import unittest
from unittest import mock
from unittest.mock import patch

from app.dtos.user_dto import UserDTO
from app.exceptions import EmailTakenError, UserNameEmptyError, InvalidPasswordError
from app.repositories.user_repository import UserRepository
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

    def test_register_user_should_succeed(self):
        # given
        user_dto = _create_user_dto(email='<EMAIL>', name='<NAME>')
        self.mock_repository.does_user_exist.return_value = False

        # when
        self.sut.register_user(user_dto)

        # then
        self.mock_repository.does_user_exist.assert_called_once_with(user_dto.email)
        self.mock_repository.create_new_user.assert_called_once_with(user_dto)
        self.assertNotEqual(user_dto.password, "<PASSWORD>")

    def test_register_user_should_throw_email_taken_error(self):
        # given
        user_dto = _create_user_dto(email='<EMAIL>', name='<NAME>')
        self.mock_repository.does_user_exist.return_value = True

        # when && then
        with self.assertRaises(EmailTakenError):
            self.sut.register_user(user_dto)
            self.mock_repository.does_user_exist.assert_called_once_with(user_dto.email)

    def test_register_user_should_throw_empty_name_error(self):
        # given
        user_dto = _create_user_dto(email='<EMAIL>', name=None)
        self.mock_repository.does_user_exist.return_value = False

        # when && then
        with self.assertRaises(UserNameEmptyError):
            self.sut.register_user(user_dto)
            self.mock_repository.does_user_exist.assert_called_once_with(user_dto.email)

    @patch('app.services.auth_service.check_password_hash')
    @patch('app.services.auth_service.create_access_token')
    def test_authenticate_user_should_succeed(self, mock_create_access_token, mock_check_password_hash):
        # given
        user_dto = _create_user_dto(email='<EMAIL>', name='<NAME>')
        token = 'token'

        mock_check_password_hash.return_value = True
        mock_create_access_token.return_value = token

        user = UserDTO(id=1, name="name", email=user_dto.email, password=user_dto.password)
        self.mock_repository.get_user_by_email.return_value = user

        # when
        access_token = self.sut.authenticate(user_dto)

        # then
        self.mock_repository.get_user_by_email.assert_called_once_with(user_dto.email)
        self.assertEqual(access_token, token)

    @patch('app.services.auth_service.check_password_hash')
    def test_authenticate_user_should_throw_invalid_password_error(self, mock_check_password_hash):
        # given
        user_dto = _create_user_dto(email='<EMAIL>', name='<NAME>')
        mock_check_password_hash.return_value = False

        user = UserDTO(id=1, name="name", email=user_dto.email, password=user_dto.password)
        self.mock_repository.get_user_by_email.return_value = user

        # when && then
        with self.assertRaises(InvalidPasswordError):
            self.sut.authenticate(user_dto)
