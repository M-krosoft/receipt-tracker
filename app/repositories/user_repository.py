import app.mappers.user_mapper as mapper
from app import db
from app.dtos.user_dto import UserDTO
from app.exceptions import UserNotExistError
from app.models.user import User


class UserRepository:
    @staticmethod
    def create_new_user(user_dto: UserDTO):
        new_user = mapper.of_dto(user_dto)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_user_by_id(user_id: int) -> UserDTO:
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise UserNotExistError
        return mapper.to_dto(user)

    @staticmethod
    def get_user_by_email(email: str) -> UserDTO:
        user = User.query.filter_by(email=email).first()
        if user is None:
            raise UserNotExistError
        return mapper.to_dto(user)

    @staticmethod
    def delete_user_by_id(user_id: int) -> None:
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise UserNotExistError
        User.query.filter_by(id=user_id).delete()
        db.session.commit()

    @staticmethod
    def update_user_password(user_id: int, new_password: str) -> None:
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise UserNotExistError
        user.password = new_password
        db.session.commit()
