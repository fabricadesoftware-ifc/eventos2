from rest_framework.exceptions import APIException


class EventosException(APIException):
    pass


class NotFoundError(EventosException):
    status_code = 404
    default_detail = "The requested resource could not be found."
    default_code = "not_found"


class DuplicateIdentifierError(EventosException):
    status_code = 409
    default_detail = "The supplied identifier has already been used."
    default_code = "duplicate_identifier"


class NotAuthorizedError(EventosException):
    status_code = 403
    default_detail = "You cannot access the requested resource."
    default_code = "forbidden"
