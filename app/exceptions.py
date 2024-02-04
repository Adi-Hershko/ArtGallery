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