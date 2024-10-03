from datetime import datetime


class UserDTO:
    def __init__(self, name: str, email: str, password: str, id: int = None, created_date: datetime = None):
        self.name = name
        self.email = email
        self.password = password
        self.id = id
        self.created_date = created_date
