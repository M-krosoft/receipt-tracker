class EmailTakenError(Exception):
    pass


class UserNotExistError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class UserNameEmptyError(Exception):
    pass


class InvalidRequestFieldError(Exception):
    pass
