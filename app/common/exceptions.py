from rest_framework.exceptions import APIException
from rest_framework import status


class UnprocessableEntityException(Exception):
    def __init__(self, message) -> None:
        self.message = message


class APIExceptionWithStatusCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad request."
    default_code = "bad request"

    def __init__(self, detail=None, code=None, status_code=None, field_name=None):
        if status_code:
            self.status_code = status_code
        if field_name and detail:
            detail = {field_name: [detail]}
        super().__init__(detail, code)
