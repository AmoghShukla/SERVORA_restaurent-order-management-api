class AppError(Exception):
    def __init__(self, message: str = "Application error", status_code: int | None = None, detail: str | None = None):
        self.status_code = status_code
        self.detail = detail or message
        super().__init__(self.detail)


class RepositoryError(AppError):
    pass


class ServiceError(AppError):
    pass


class NotFoundError(RepositoryError):
    pass


class AlreadyExistsError(ServiceError):
    pass