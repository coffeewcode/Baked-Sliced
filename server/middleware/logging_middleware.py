import time
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        log_data = {
            "type": "request",
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration": duration,
            "client_ip": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
        }
        logger.info(log_data)
        return response
