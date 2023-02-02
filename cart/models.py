from django.db import models
from django.contrib.auth.models import User
from gaming_products.models import Product,Category,SubCategory,AllModels
# Create your models here.
from django.conf import settings
User = settings.AUTH_USER_MODEL    


class CheckoutCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=True)
    cart = models.ManyToManyField(AllModels,related_name='cart')
    quantity = models.PositiveIntegerField(default=1, blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0) 
    created_at = models.DateTimeField(auto_now=True)