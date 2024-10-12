from datetime import datetime

from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app.dtos.user_dto import UserDTO
from app.exceptions import EmailTakenError, InvalidPasswordError, UserNameEmptyError
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, user_dto: UserDTO) -> None:
        if self.repository.does_user_exist(user_dto.email):
            raise EmailTakenError

        if user_dto.name is None or user_dto.name == "":
            raise UserNameEmptyError

        user_dto.password = generate_password_hash(user_dto.password)
        user_dto.created_date = datetime.now()
        self.repository.create_new_user(user_dto)

    def authenticate(self, user_dto: UserDTO) -> str:
        user = self.repository.get_user_by_email(user_dto.email)
        if not check_password_hash(user.password, user_dto.password):
            raise InvalidPasswordError

        access_token = create_access_token(identity=user.id)
        return access_token
