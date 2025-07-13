import logging
from django.http import JsonResponse
from utils.jwt import JWT
from fnmatch import fnmatch
from config.settings import SKIP_VERIFICATION
from constants.constant import TokenType


logger = logging.getLogger('whisper')



class JWTMiddleware:
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
        
        auth_token = request.headers.get('Authorization')
        
        if(not auth_token):
            return JsonResponse({"message": "Access token not given"}, status=403)
        
        token=auth_token.split(" ")[1]

        if(not token):
            return JsonResponse({"message": "Invalid Token"}, status=403)
        decoded=JWT.verify_jwt(token=token)
        token_data=decoded["data"]
        if not token_data:
            return JsonResponse({"message":decoded["message"]},status=401) 
        
        if token_data["type"] != TokenType.ACCESS:
            return JsonResponse({"message": "Access token is not valid"}, status=403)

        request.email = token_data["email"]
        request.role=token_data['role']
        response = self.get_response(request)
        return response
        