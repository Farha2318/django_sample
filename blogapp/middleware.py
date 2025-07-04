# blogapp/middleware.py
import logging

logger = logging.getLogger(__name__)

class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        path = request.path
        logger.info(f"Request path: {path}, IP: {ip}")
        response = self.get_response(request)
        return response
