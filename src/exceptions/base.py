class ServiceError(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class NotFoundError(ServiceError):
    pass


class AlreadyExistsError(ServiceError):
    pass
