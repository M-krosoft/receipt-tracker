from app import mapper, db
from app.dtos import UserDTO
from app.models.user import User


def create_new_user(user_dto: UserDTO):
    new_user = mapper.of_dto(user_dto)
    db.session.add(new_user)
    db.session.commit()


def get_user_by_id(user_id: int) -> UserDTO:
    user = User.query.filter_by(id=user_id).first()
    return mapper.to_dto(user)


def get_user_by_email(email: str) -> UserDTO:
    user = User.query.filter_by(email=email).first()
    return mapper.to_dto(user)


def delete_user_by_id(user_id: int) -> None:
    User.query.filter_by(id=user_id).delete()
    db.session.commit()


def update_user_password(user_id: int, new_password: str) -> None:
    user = User.query.filter_by(id=user_id).first()
    user.password = new_password
    db.session.commit()
