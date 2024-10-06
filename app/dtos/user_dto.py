from datetime import datetime


class UserDTO:
    def __init__(self,  id: int = None, name: str = "", email: str = "", password: str = "", created_date: datetime = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.created_date = created_date
