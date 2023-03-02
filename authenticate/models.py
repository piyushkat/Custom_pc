from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.core.validators import RegexValidator
from django.conf import settings
# Create your models here.
 
class CustomUser(AbstractUser):
    phone_no = models.CharField(
    max_length=16,
    validators=[
      RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format '+123456789'. Up to 15 digits allowed."
      ),
    ],
  )
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['username','first_name','last_name','password','phone_no']


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,blank=False, primary_key=True,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)