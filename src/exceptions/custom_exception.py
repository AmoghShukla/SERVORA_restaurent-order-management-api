class RepositoryError(Exception):
    pass

class ServiceError(Exception):
    pass

class NotFoundError(RepositoryError):
    pass

class AlreadyExistsError(ServiceError):
    pass