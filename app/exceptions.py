class UserNotFoundException(Exception):
    def __init__(self, message="User not found", status_code=404):
        self.status_code = status_code
        super().__init__(message)

class PasswordNotMatchException(Exception):
    def __init__(self, message="Password does not match", status_code=401):
        self.status_code = status_code
        super().__init__(message)
