class ServiceError(Exception):
    def __init__(self, detail: str | None = None):
        self.detail = detail


class NotFoundError(ServiceError):
    pass


class ForbiddenError(ServiceError):
    pass


class AlreadyExistsError(ServiceError):
    pass
