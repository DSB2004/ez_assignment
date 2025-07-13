
from rest_framework import status,viewsets
from rest_framework.response import Response
from .models import User,Role


from utils.hashing import Hashing
from utils.otp import OTP
from utils.url import URL
from utils.jwt import JWT
from service.mail import MailService
from constants.constant import TokenType,VerificationAction  # constants


class LoginViewSet(viewsets.ViewSet):
    def create(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        client_callback_url=request.data.get("client_callback_url")
        if not email or not password or not client_callback_url:
            return Response({"message": "Email, client callback url and password required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user=User.objects.get(email=email)
            if(Hashing.check_password(password=password,hashed=user.password)==False):
                return Response({"message":"Incorrect Password"},status=400)
            if(user.is_verified==False):
                verification_token=URL.generate_url(email=email,action=VerificationAction.ACCOUNT_VERIFICATION)
                verification_url=f"{client_callback_url}?access_token={verification_token}&email={email}"
                MailService.send_mail.delay(email=user.email,content=verification_url)
                return Response({"message":"Please verify your account","url":verification_url},status=403)
        except user.DoesNotExist:
            return Response({"message":f"No account registered to {email}"},status=400)

        try:
            access_token_data={
                "email":email,
                "type":TokenType.ACCESS,
                "role":user.role
            }   
            refresh_token_data={
                "email":email,
                "type":TokenType.REFRESH,
            }    
            
            access_token=JWT.generate_jwt(access_token_data,3600*24) 
            refresh_token=JWT.generate_jwt(refresh_token_data,7*24*3600) 
            return Response({"message":"Login successful","role":user.role,"email":email, "access_token":access_token,"refresh_token":refresh_token},status=200)
        except User.DoesNotExist:
            return Response({"message":"Internal Server Error"},status=500)
        
    


class SignUpViewSet(viewsets.ViewSet):
    def create(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        client_callback_url=request.data.get("client_callback_url")
        if not email or not password or not client_callback_url:
            return Response({"message": "Email ,client callback url and password required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user=User.objects.get(email=email)
            if user:
                return Response({"message":"User already exist"},status=400)
        except User.DoesNotExist:
            pass
        try:
            hashed_password=Hashing.hash_password(password=password)
            User.objects.create(email=email,password=hashed_password,role=Role.CLIENT)
            verification_token=URL.generate_url(email=email,action=VerificationAction.ACCOUNT_VERIFICATION)
            verification_url=f"{client_callback_url}?access_token={verification_token}&email={email}"
            MailService.send_mail.delay(email=email,content=verification_url)
            return Response({"message":"Signup Successful!! Please verify your account","role":Role.CLIENT,"email":email,"url":verification_url },status=200)
        except Exception as e:
            print(e)
            return Response({"message":"Internal Server Error"},status=500)
        


class RequestVerificationViewSet(viewsets.ViewSet):
    def create(self,request):
        email=request.data.get("email")
        client_callback_url=request.data.get("client_callback_url")
        if not email or client_callback_url: 
            return Response({"message":"Email and client callback url are required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            verification_token=URL.generate_url(email=email,action=VerificationAction.ACCOUNT_VERIFICATION)
            verification_url=f"{client_callback_url}?access_token={verification_token}&email={email}"
            MailService.send_mail.delay(email=email,content=verification_url)
            return Response({"message":"Your account has been verified","url":verification_url},status=200)

        except User.DoesNotExist:
            return Response({"message":f"No account registered to {email}"},status=400)
        except Exception as e:
            return Response({"message":"Internal Server Error"},status=500)
        

class VerifyAccountViewSet(viewsets.ViewSet):
    def list(self,request):
        access_token=request.query_params.get("access_token")
        email=request.query_params.get("email")

        if not access_token or not email:
            return Response({"message":"Access token and email are required"}, status=status.HTTP_401_UNAUTHORIZED)
        

        try:
            res=URL.verify_url(token=access_token,email=email,action=VerificationAction.ACCOUNT_VERIFICATION)
            success=res.get('success',False)
            message=res.get('message','Verification Failed')

            if(success==False):
                return Response({"message":message}, status=status.HTTP_401_UNAUTHORIZED)
            
            user=User.objects.get(email=email)
            user.is_verified=True
            user.save()

            access_token_data={
                "email":email,
                "type":TokenType.ACCESS,
                "role":Role.CLIENT
            }   
            refresh_token_data={
                "email":email,
                "type":TokenType.REFRESH,
            }    
            
            access_token=JWT.generate_jwt(access_token_data,3600*24) 
            refresh_token=JWT.generate_jwt(refresh_token_data,7*24*3600) 
            

            return Response({"message":"Your account has been verified","refresh_token":refresh_token,"access_token":access_token,"role":user.role,"email":user.email},status=200)

        except User.DoesNotExist:
            return Response({"message":f"No account registered to {email}"},status=400)
        except Exception as e:
            return Response({"message":"Internal Server Error"},status=500)
        
    



class ForgetPasswordViewSet(viewsets.ViewSet):
    def create(self,request):
        email = request.data.get('email')
        client_callback_url=request.data.get("client_callback_url")
        if not email or not client_callback_url:
            return Response({"message": "email and client callback url required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(email=email)
            verification_token=URL.generate_url(email=email,action=VerificationAction.RESET_PASSWORD)
            verification_url=f"{client_callback_url}?access_token={verification_token}&email={email}"
            MailService.send_mail.delay(email=email,content=verification_url)
            return Response({"message":f"Password reset email has been sent to {email}","url":verification_url},status=200)
        
        except User.DoesNotExist:
            return Response({"message":f"No account registered to {email}"},status=400)
        except Exception:
            return Response({"message":"Internal Server Error"},status=500)
        

    



class ResetPasswordViewSet(viewsets.ViewSet):
    def create(self,request):
        access_token=request.query_params.get("access_token")
        email = request.data.get('email')
        password=request.data.get('password')

        if not email or not access_token or not password:
            return Response({"message": "email, access_token and action  required"}, status=status.HTTP_400_BAD_REQUEST)
        
        res=URL.verify_url(token=access_token,email=email,action=VerificationAction.RESET_PASSWORD)
        success=res.get('success',False)
        email=res.get("email",'')
        message=res.get('message','Verification Failed')

        if(success==False):
            return Response({"message":message}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user=User.objects.get(email=email)
            hash_password=Hashing.hash_password(password=password)
            user.password=hash_password
            user.save()
            return Response({"message":"Password reset"},status=200)
        except user.DoesNotExist:
            return Response({"message":f"No account registered to {email}"},status=400)
        except Exception:
            return Response({"message":"Internal Server Error"},status=500)
        


class RefreshTokenViewSet(viewsets.ViewSet):
    def create(self,request):
        refresh_token=request.data.get("refresh_token") 

        token=refresh_token.split(" ")
        if not refresh_token or token[0]!='Bearer':
            return Response({"message": "Refresh token required or invalid"}, status=status.HTTP_400_BAD_REQUEST)
        
        decoded=JWT.verify_jwt(token=token[1])

        token_data=decoded["data"]
        if not token_data:
            return Response({"message":decoded["message"]},status=401) 
        email=token_data["email"]


        try:
            user=User.objects.get(email=email)
            access_token_data={
                "email":email,
                "type":TokenType.ACCESS,
                "role":user.role
            }   
            refresh_token_data={
                "email":email,
                "type":TokenType.REFRESH,
            }    
            
            access_token=JWT.generate_jwt(access_token_data,3600*24) 
            refresh_token=JWT.generate_jwt(refresh_token_data,7*24*3600) 
            return Response({"message":"Session refreshed", "access_token":access_token,"refresh_token":refresh_token},status=200)
            
        except user.DoesNotExist:
            return Response({"message":f"No account registered to {email}"},status=400)
        except Exception:
            return Response({"message":"Internal Server Error"},status=500)
        
        
    