class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    def __init__(self, message: str = "resource_not_found"):
        super().__init__(message=message, status_code=404)


class ForbiddenError(AppException):
    def __init__(self, message: str = "forbidden"):
        super().__init__(message=message, status_code=403)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "unauthorized"):
        super().__init__(message=message, status_code=401)
