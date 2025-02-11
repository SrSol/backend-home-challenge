class DomainException(Exception):
    pass

class EntityNotFoundException(DomainException):
    pass

class ValidationException(DomainException):
    pass

class UnauthorizedException(DomainException):
    pass
