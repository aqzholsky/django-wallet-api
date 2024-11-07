import traceback

from django.conf import settings

from rest_framework import status

from .exceptions import APIExceptionWithStatusCode, UnprocessableEntityException


class APIHandleExceptionMixin:
    def handle_exception(self, exc):
        if settings.DEBUG:
            traceback.print_exc()

        if isinstance(exc, UnprocessableEntityException):
            exc = APIExceptionWithStatusCode(
                detail=exc.message, code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        return super(APIHandleExceptionMixin, self).handle_exception(exc)
