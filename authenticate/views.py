from django.shortcuts import render
from rest_framework.generics import GenericAPIView
import environ
import datetime
import environ
import requests
from rest_framework.response import Response
from rest_framework import status
from authenticate.serializer import *
from authenticate.renderer import UserRenderer
from django.contrib.auth.hashers import check_password,make_password
from rest_framework.permissions import IsAuthenticated
from authenticate.helper import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import datetime, timedelta
# Create your views here.

# importing and cofigure dot env file
env=environ.Env()
environ.Env.read_env()
EMAIL_FROM = env('EMAIL_FROM')


# validation for unique user email
def unique_email(email):
  """
  :return: All the users have the unique Email id.
  """
  res = User.objects.filter(email = email) # Get the Email from the User table. 
  return res


# generate token using simple jwt token 
def get_tokens_for_user(user):
  """
  :return: refresh and access token generate when the user hit the login api.
  """
  refresh = RefreshToken.for_user(user) # Give the refresh token for the user
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
}


class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    renderer_classes = [UserRenderer]
    def post(self,request):
        confirm_password = request.data.get('password1') #Request the Email from the user)
        email = request.data.get('email') #Request the Email from the user
        password = request.data.get('password') # Request the password from the user
        first_name = request.data.get('first_name') # Request th0e first name from the user
        last_name = request.data.get('last_name') # Request the last name from the user
        phone_no = request.data.get('phone_no')
        pass_bool = Validate_Password(password) # Validate the password.
        if not pass_bool:
            return Response({'msg': 'Enter valid passoword'})
        res = unique_email(email) # Email is unique for every user.
        if res:
            return Response({'msg': 'Email or username already Exists'})
        if password!=confirm_password:
            return Response({'msg': 'Password doesnot match'})
        serializer = UserRegistrationSerializer(data=request.data) # serializer the data
        serializer.is_valid(raise_exception=True) # if fields is valid
        user = User.objects.create(username=email,password=password,email=email,first_name=first_name,last_name=last_name,phone_no=phone_no)
        user.password= make_password(password)
        user.save()
        otp = email_otp() # six digits otp send to your email.
        user_obj = User.objects.get(username=email) # Get the username from the user table.
        profile = Profile(user=user_obj,auth_token=otp)
        profile.save()
        # sending otp in user email while register
        EMAIL_FROM = env('EMAIL_FROM')
        EMAIL_FROM = env('EMAIL_FROM')
        subject = 'Verify Email Otp '
        message = f'Hi {first_name,last_name}, OTP for Email Verification is {otp}.'
        email_from = EMAIL_FROM
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list)
        return Response({'msg':'Registration Successfull, A OTP Verification code has been send to your Email'}, status = 201)


class VerifyOtp(GenericAPIView):
  serializer_class = VerifyOtpSerializer
  renderer_classes = [UserRenderer]
  def post(self,request):
    """
    :return: Send OTP through Email When the user hit the register api. 
    """
    user = request.data.get('user')
    auth_token = request.data.get('auth_token')
    if not user or not auth_token:
      return Response({'msg': 'Invalid parameters'})
    res = Profile.objects.filter(user_id=user).values()
    if res:  #checks if there is any user with this id
      otp_time=res[0]['created_at']
      time_change = timedelta(days=1)
      new_time=otp_time+time_change
      now = datetime.now(timezone.utc)
      if new_time>= now:
          if str(res[0]['user_id'])==user and res[0]['auth_token']==auth_token:
            res.update(is_verified=True)
            return Response({"status": "Otp Verified"}, status = 200)
          return Response({"status": "Otp Incorrect"}, status = 400)
      return Response({"status": "Verification OTP Expired"}, status = 400)
    return Response({"status": "No user found"}, status = 400)


class VerifyEmailOtpSecondTime(GenericAPIView):
  serializer_class = VerifyOtpSerializer
  renderer_classes = [UserRenderer]
  def post(self,request):
    """
    :return: send OTP second time for email verification when user is to forgot to Enter the OTP for first time.
    """
    email = request.data.get('email') # Enter the same mail you enter registration time
    if not email: # check the parameter of the email
      return Response({'msg': 'Invalid parameters'})
    res = User.objects.filter(email=email).values('id') # Get the Email from the user table
    if res:
      otp = email_otp() # six digits otp send to your email.
      EMAIL_FROM = env('EMAIL_FROM')
      EMAIL_FROM = env('EMAIL_FROM')
      subject = 'Verify Email Otp '
      message = f'Hi {email}, OTP for Email Verification is {otp}.'
      email_from = EMAIL_FROM
      recipient_list = [email]
      send_mail( subject, message, email_from, recipient_list) # send otp thrugh email if the email is stored in the database
      profile  = Profile.objects.get(user=res[0]['id'])
      profile.auth_token=otp
      profile.created_at=datetime.datetime.now(timezone.utc)
      profile.save()
      return Response({'msg':' A Verification code has been send to your Email'}, status = 201)
    return Response({'msg':"Email Doesn't exists"}, status = 204)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    renderer_classes = [UserRenderer]
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"msg":"Email Password Incorrect"})
        user = User.objects.filter(email=email).values('id','is_superuser')
        if user:
            if not user[0]['is_superuser']:
                try:
                    res=Profile.objects.get(user=user[0]['id'])
                except:
                    return Response({'msg':'Please continue with google to login'})
                if res:
                    if res.is_verified == False:
                        return Response({'msg': 'email not verified'})
                serializer = UserLoginSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = authenticate(email=email,password=password)
                if user is not None:
                    token = get_tokens_for_user(user)
                    return Response({'token': token, 'msg': 'Login Success'})
                else:
                    return Response({'errors': {'non_field_errors': ['Username or Password is not Valid']}}, status = 404)
        return Response({'msg': 'No user found'}, status = 404)


class SendPasswordEmailView(GenericAPIView):
  serializer_class = SendPasswordResetEmailSerializer
  renderer_classes = [UserRenderer]
  def post(self, request, formate=None):
    """
    :return: Reset password email successfully send.
    """
    serializers = SendPasswordResetEmailSerializer(data=request.data)
    serializers.is_valid(raise_exception=True)
    return Response({'msg':'Email Sent Successful'}, status = 200)


# user reset password view
class UserPasswordResetView(GenericAPIView):
  serializer_class = UserPasswordResetSerializer
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    """
    :return: Password reset through Email when the user forgot the pasword.
    """
    serializers = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token, 'user':request.user})
    serializers.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successful'}, status = 200)


class UserChangePasswordView(GenericAPIView):
  serializer_class = UserChangePasswordSerializer
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    """
    :return: password change when the user is logged in.
    """
    fields = ('old_password','password')
    for field  in request.data.keys():
      if field not in fields:
        return Response({'msg': 'Fields Incorrect'})
    old_password =request.data.get('old_password')
    password =request.data.get('password')
    id = self.request.user.id
    pass_get = User.objects.filter(id=id).values('password')
    if check_password(old_password,pass_get[0]['password']): 
      # serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
      # serializer.is_valid(raise_exception=True)
      user_object=User.objects.get(id=id)
      user_object.password= make_password(password)
      user_object.save() 
      return Response({'msg':'Password Changed Successfully'}, status = 200)
    return Response({'msg':'Old Password entered incorrectly '}, status=403)

  
class UpdateUserProfile(GenericAPIView):
  serializer_class = UserUpdateProfileSerializer
  renderer_classes = [UserRenderer]
  def put(self, request, id):
    try:
      user = User.objects.get(id=id)
      serializer = UserUpdateProfileSerializer(user, data=request.data)
      serializer.is_valid()
      serializer.save()
      return Response({"status":"success", "data": serializer.data}, status = 200)
    except:
      return Response({"status":"User Not Found"}, status = 400)


class DeleteUserProfile(GenericAPIView):
  renderer_classes = [UserRenderer]
  def delete(self, request,id):
    try:
      user = User.objects.get(id=id) 
      user.delete()
      return Response({"status":"User Deleted Successfully"},status=200)
    except:
      return Response({"status":"User Not Found"}, status = 400)



