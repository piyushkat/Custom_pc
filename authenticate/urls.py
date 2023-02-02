from django.urls import path,include
from authenticate.views import *

urlpatterns = [
    path('signup',UserRegistrationView.as_view(), name='signup'),
    path('verifyotp',VerifyOtp.as_view(), name='verifyotp'),
    path('verifyemail',VerifyEmailOtpSecondTime.as_view(), name='verifyemail'),
    path('signin',UserLoginView.as_view(), name='signin'),
]
