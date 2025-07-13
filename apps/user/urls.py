from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginViewSet,SignUpViewSet,ForgetPasswordViewSet,ResetPasswordViewSet,VerifyAccountViewSet,RefreshTokenViewSet,RequestVerificationViewSet

router=DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')
router.register(r'signup', SignUpViewSet, basename='signup')
router.register(r'verify', VerifyAccountViewSet, basename='verify')
router.register(r'forget', ForgetPasswordViewSet, basename='forget')
router.register(r'reset', ResetPasswordViewSet, basename='reset')
router.register(r'refresh',RefreshTokenViewSet,basename="refresh")
router.register(r'request-verification',RequestVerificationViewSet,basename="request-verification")

urlpatterns = [
    path('', include(router.urls)),
]