from django.conf import settings
import traceback
from .exceptions import (
    UnprocessableEntityException,
    APIExceptionWithStatusCode,
)
from rest_framework import status


class APIHandleExceptionMixin:
    def handle_exception(self, exc):
        if settings.DEBUG:
            traceback.print_exc()

        if isinstance(exc, UnprocessableEntityException):
            exc = APIExceptionWithStatusCode(
                detail=exc.message, code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        return super(APIHandleExceptionMixin, self).handle_exception(exc)
