class UserNotFoundException(Exception):
    pass

class PasswordNotMatchException(Exception):
    pass

class PostNotFoundException(Exception):
    pass

class FeedNotFoundException(Exception):
    pass

class OperationError(Exception):
    pass

class UserAlreadyExist(Exception):
    pass

class PasswordTooShort(Exception):
    pass

class PasswordTooLong(Exception):
    pass

class UsernameTooShort(Exception):
    pass

class UsernameTooLong(Exception):
    pass

class ImageAlreadyExists(Exception):
    pass
