from app.dtos.user_dto import UserDTO
from app.models.user import User


def of_dto(user_dto: UserDTO) -> User:
    return User(
        name=user_dto.name,
        email=user_dto.email,
        password=user_dto.password,
        id=user_dto.id,
        created_date=user_dto.created_date
    )


def to_dto(user: User) -> UserDTO:
    return UserDTO(
        name=user.name,
        email=user.email,
        password=user.password,
        id=user.id,
        created_date=user.created_date
    )
