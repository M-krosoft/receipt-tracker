from datetime import datetime, timedelta

from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from app.dtos.user_dto import UserDTO
from app.exceptions import EmailTakenError, InvalidPasswordError, UserNameEmptyError
from app.repositories.user_repository import UserRepository
from app.requests import RegisterRequest, LoginRequest


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, register_request: RegisterRequest) -> None:
        if self.repository.does_user_exist(register_request.email):
            raise EmailTakenError(email=register_request.email)

        if register_request.name is None or register_request.name == "":
            raise UserNameEmptyError

        user_dto = UserDTO()
        user_dto.name = register_request.name
        user_dto.email = register_request.email
        user_dto.password = generate_password_hash(register_request.password)
        user_dto.created_date = datetime.now()

        self.repository.create_new_user(user_dto)

    def authenticate(self, login_request: LoginRequest) -> str:
        user = self.repository.get_user_by_email(login_request.email)
        if not check_password_hash(user.password, login_request.password):
            raise InvalidPasswordError

        expires = timedelta(days=30)
        access_token = create_access_token(identity=user.id, expires_delta=expires)
        return access_token
