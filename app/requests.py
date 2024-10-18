class RegisterRequest:
    def __init__(self, name: str = None, email: str = None, password: str = None, ):
        self.name = name
        self.email = email
        self.password = password


class LoginRequest:
    def __init__(self, email: str = None, password: str = None):
        self.email = email
        self.password = password
