import secrets
import redis
from config import settings
import json
from constants.constant import VerificationError
redis_client = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)

class OTP:

    def generate_otp(email, action,length=6):
        code = ''.join(secrets.choice("0123456789") for _ in range(length))
        key = f"verify:{code}"
        value = json.dumps({
            "email": email,
            "action": action
        })
        redis_client.setex(key, 600, value) 
        return code

    @staticmethod
    def verify_otp(email,action,code):
        key = f"verify:{code}"
        data = redis_client.get(key)

        if data is None:
            return {
                "success": False,
                "code":VerificationError.SESSION,
                "message": "Expired Session"
            }

        try:
            info = json.loads(data)
            email_ = info.get("email")
            action_ = info.get("action")
        except Exception:
            return {
                "success": False,
               "code":VerificationError.SESSION,
                "message": "Expired Session"
            }
        
        
        if(action!=action_):
             return {
                "success": False,
                "code":VerificationError.INVALID,
                "message": "Invalid Action"
            }

        if(email!=email_):
             return {
                "success": False,
                "code":VerificationError.INVALID,
                "message": "Invalid Action"
            }
            
        # redis_client.delete(key)
        
        return {
            "success": True,
            "message": "Verification successful",
        }
    