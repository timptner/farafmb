import logging
from django.http import HttpRequest, HttpResponse
from typing import Callable

logger = logging.getLogger(__name__)


class LogRequestMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        self.log_request(request)
        response = self.get_response(request)
        return response

    def log_request(self, request: HttpRequest) -> None:
        logger.info(f"Request URL: {request.path}")
        logger.info(f"Method: {request.method}")
        logger.info(f"Client IP: {request.META.get('REMOTE_ADDR')}")

        for header, value in request.headers.items():
            logger.info(f"Header: {header} = {value}")
