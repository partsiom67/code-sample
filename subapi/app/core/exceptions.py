class DatabaseConnectionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidIdException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass


class UserUnauthorizedException(Exception):
    pass


class TokenExpiredSignatureException(UserUnauthorizedException):
    pass


class TokenInvalidSignatureException(UserUnauthorizedException):
    pass


class SubscriptionNotFoundException(Exception):
    pass


class SubscriptionAlreadyExistsException(Exception):
    pass


class TopicNotFoundException(Exception):
    pass


class TopicAlreadyExistsException(Exception):
    pass


class ItemNotFoundException(Exception):
    pass
