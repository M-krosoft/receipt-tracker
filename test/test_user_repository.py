import unittest

import app.repositories.user_repository as sut
from app import create_app, db
from app.app_config import TestingConfig
from app.dtos.user_dto import UserDTO
from app.models.user import User


def _save_user_and_return() -> User:
    user = User(
        email='<EMAIL>',
        name='<NAME>',
        password='<PASSWORD>'
    )
    db.session.add(user)
    db.session.commit()
    return User.query.filter_by(email=user.email).first()


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.config = TestingConfig()
        self.app = create_app(config=self.config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

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
        sut.create_new_user(user_dto)

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
        user = _save_user_and_return()
        # when
        result = sut.get_user_by_id(1)
        # then
        self._assert_dto_equals_user(result, expected=user)

    def test_get_user_by_email(self):
        # given
        user = _save_user_and_return()
        # when
        result = sut.get_user_by_email(user.email)
        # then
        self._assert_dto_equals_user(result, expected=user)

    def test_delete_user_by_id(self):
        # given
        user_to_del = _save_user_and_return()
        # when
        sut.delete_user_by_id(user_id=user_to_del.id)
        # then
        deleted = User.query.filter_by(id=user_to_del.id).first()
        self.assertIsNone(deleted)

    def test_update_user_password(self):
        # given
        user_to_update = _save_user_and_return()
        new_password = '<PASSWORD-CHANGED>'
        # when
        sut.update_user_password(user_id=user_to_update.id, new_password=new_password)
        # then
        updated = User.query.filter_by(id=user_to_update.id).first()
        self.assertIsNotNone(updated)
        self.assertEqual(updated.password, new_password)

    def _assert_dto_equals_user(self, result: UserDTO, expected: User) -> None:
        self.assertIsNotNone(result)
        self.assertEqual(result.id, expected.id)
        self.assertEqual(result.created_date, expected.created_date)
        self.assertEqual(result.email, expected.email)
        self.assertEqual(result.name, expected.name)
        self.assertEqual(result.password, expected.password)
