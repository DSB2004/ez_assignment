import logging

logger = logging.getLogger('whisper')

class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"{request.method} {request.path}")

        response = self.get_response(request)

        if(response.status_code not in [200,201,202]):
            logger.warning(f"{request.method} {request.path} {response.status_code}")
        else:
            logger.info(f"{request.method} {request.path} {response.status_code}")           
        return response