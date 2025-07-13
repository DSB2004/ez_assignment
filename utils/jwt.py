import jwt
from datetime import datetime, timedelta, timezone
from config.settings import ALGORITHMS,JWT_SECRET
class JWT:

    def generate_jwt(payload, expires_in=30):
        now = datetime.now(timezone.utc)
        exp = now + timedelta(minutes=expires_in)

        payload = {
            **payload,
            "exp": int(exp.timestamp()),  
            "iat": int(now.timestamp()) 
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHMS)
        return "Bearer " + token 

    def verify_jwt(token:str):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHMS])
            return {"data":payload,"message":"Token decoded successfully"}
        except jwt.ExpiredSignatureError:
            return {"data":None,"message":"Token Expired"}
        except jwt.InvalidTokenError:
            return {"data":None,"message":"Invalid Token"}
