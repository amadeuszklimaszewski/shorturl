class ApplicationError(Exception):
    pass


class AlreadyExistsError(ApplicationError):
    pass


class DoesNotExistError(ApplicationError):
    pass
