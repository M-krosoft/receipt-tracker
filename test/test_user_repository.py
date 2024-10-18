import unittest

from app import create_app, db
from app.app_config import TestingConfig
from app.dtos.user_dto import UserDTO
from app.exceptions import UserNotExistError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from test.models_factory import ModelsFactory


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.config = TestingConfig()
        self.app = create_app(config=self.config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.sut = UserRepository()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_new_user(self):
        # given
        user_dto = UserDTO(
            name='<NAME>',
            email='<EMAIL>',
            password='<PASSWORD>'
        )

        # when
        self.sut.create_new_user(user_dto)

        # then
        saved_user = User.query.filter_by(email=user_dto.email).first()
        self.assertIsNotNone(saved_user)
        self.assertIsNotNone(saved_user.id)
        self.assertIsNotNone(saved_user.created_date)
        self.assertEqual(saved_user.password, user_dto.password)
        self.assertEqual(saved_user.email, user_dto.email)
        self.assertEqual(saved_user.name, user_dto.name)

    def test_get_user_by_id(self):
        # given
        user = ModelsFactory.create_user_in_db()
        # when
        result = self.sut.get_user_by_id(1)
        # then
        self._assert_dto_equals_user(result, expected=user)

    def test_get_user_by_email(self):
        # given
        user = ModelsFactory.create_user_in_db()
        # when
        result = self.sut.get_user_by_email(user.email)
        # then
        self._assert_dto_equals_user(result, expected=user)

    def test_delete_user_by_id(self):
        # given
        user_to_del = ModelsFactory.create_user_in_db()
        # when
        self.sut.delete_user_by_id(user_id=user_to_del.id)
        # then
        deleted = User.query.filter_by(id=user_to_del.id).first()
        self.assertIsNone(deleted)

    def test_update_user_password(self):
        # given
        user_to_update = ModelsFactory.create_user_in_db()
        new_password = '<PASSWORD-CHANGED>'
        # when
        self.sut.update_user_password(user_id=user_to_update.id, new_password=new_password)
        # then
        updated = User.query.filter_by(id=user_to_update.id).first()
        self.assertIsNotNone(updated)
        self.assertEqual(updated.password, new_password)

    def test_get_user_by_id_should_throw(self):
        # when && then
        with self.assertRaises(UserNotExistError):
            self.sut.get_user_by_id(123)

    def test_get_user_by_email_shold_throw(self):
        # when && then
        with self.assertRaises(UserNotExistError):
            self.sut.get_user_by_email('any email')

    def test_delete_user_by_id_should_throw(self):
        # when && then
        with self.assertRaises(UserNotExistError):
            self.sut.delete_user_by_id(123)

    def test_update_user_password_shold_throw(self):
        # when && then
        with self.assertRaises(UserNotExistError):
            self.sut.update_user_password(123, new_password='<PASSWORD>')

    def test_user_exist_should_return_true(self):
        # given
        user = ModelsFactory.create_user_in_db()
        # when
        result = self.sut.does_user_exist(user.email)
        # then
        self.assertTrue(result)

    def test_user_exist_should_return_false(self):
        # when
        result = self.sut.does_user_exist('any email')
        # then
        self.assertFalse(result)

    def _assert_dto_equals_user(self, result: UserDTO, expected: User) -> None:
        self.assertIsNotNone(result)
        self.assertEqual(result.id, expected.id)
        self.assertEqual(result.created_date, expected.created_date)
        self.assertEqual(result.email, expected.email)
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.password, expected.password)
