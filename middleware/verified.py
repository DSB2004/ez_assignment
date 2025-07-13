import logging
from django.http import JsonResponse
from utils.jwt import JWT
from fnmatch import fnmatch
from config.settings import SKIP_VERIFICATION
from constants.constant import TokenType

from apps.user.models import User
logger = logging.getLogger('whisper')



class EmailVerifiedMiddleware:
    @staticmethod
    def skip(method, path):
        for allowed_method, pattern in SKIP_VERIFICATION:
            if (allowed_method == "*" or method.upper() == allowed_method.upper()) and fnmatch(path, pattern):
                return True
        return False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if(self.skip(request.method,request.path)):
            response = self.get_response(request)
            return response
        
        email=request.email
        try:
            user=User.objects.get(email=email)
            if user.is_verified==False:
                return JsonResponse({"message":"User email has not been verified"},status=403)
        except User.DoesNotExist:
            return JsonResponse({"message":"User not found"},status=404)
        response = self.get_response(request)
        return response
        