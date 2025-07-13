  
import secrets
import redis
from config import settings
import json
from constants.constant import VerificationError,VerificationAction
from utils.jwt import JWT
redis_client = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)

class URL:

    @staticmethod
    def generate_url(email, action):
        key = f"verify:{email}"
        value = json.dumps({
            "email": email,
            "action": action
        })
        redis_client.setex(key, 600, value) 
        
        encrypted_token=JWT.generate_jwt({"email":email},500) # Verification link active only for 5 minutes 

        return encrypted_token.split(" ")[1]
    
    @staticmethod
    def verify_url(token,email,action):

        decoded=JWT.verify_jwt(token)
        
        if not decoded["data"]:
            return {
                "success": False,
                "code":VerificationError.SESSION,
                "message": "This verification session has been expired! Please request a new one"
            }
        data=decoded["data"]
        key = f"verify:{decoded["data"]["email"]}"
        data = redis_client.get(key)

        if data is None:
            return {
                "success": False,
                "code":VerificationError.SESSION,
        
                "message": "This verification session has been expired! Please request a new one"
            }
        try:
            info = json.loads(data)
            email_ = info.get("email")
            token_action = info.get("action")
        except Exception:
            return {
                "success": False,
               "code":VerificationError.SESSION,
                "message": "This verification session has been expired! Please request a new one"
            }
        
        
        if(action!=token_action):
             return {
                "success": False,
                "code":VerificationError.INVALID,
                "message": "This verification session is invalid! Please request a new one"
            }

        if(email!=email_):
             return {
                "success": False,
                "code":VerificationError.INVALID,
                "message":"This verification session is invalid! Please request a new one"
            }
            
        redis_client.delete(key)
        
        return {
            "success": True,
            "email": email,
            "message": "Verification successful",
        }
    