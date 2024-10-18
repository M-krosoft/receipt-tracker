class EmailTakenError(Exception):
    def __init__(self, email):
        super().__init__(f"Email '{email}' is already taken!")


class UserNotExistError(Exception):
    def __init__(self):
        super().__init__("User is not found!")


class InvalidPasswordError(Exception):
    def __init__(self):
        super().__init__("Password is invalid!")


class InvalidRequestFieldError(Exception):
    def __init__(self):
        super().__init__("Invalid request fields!")


class UserNameEmptyError(Exception):
    pass
