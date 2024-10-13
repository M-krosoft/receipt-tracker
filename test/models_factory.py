from faker import Faker

from app import db
from app.models.user import User

fake = Faker()


class ModelsFactory:

    @staticmethod
    def save_user_and_return(password=None) -> User:
        if password is None:
            password = fake.password()
        user = User(
            email=fake.email(),
            name=fake.name(),
            password=password
        )
        db.session.add(user)
        db.session.commit()
        return User.query.filter_by(email=user.email).first()
