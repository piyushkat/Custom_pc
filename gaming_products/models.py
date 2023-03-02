import random
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,default=None)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories',blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000,default=None)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subcategory',null=True,blank=True,default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category',null=True,blank=True,default=None)
    quantity = models.IntegerField()
    in_stock = models.BooleanField(default=False)
    price = models.IntegerField(default=None)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description':self.description,
            'price':self.price


            # other fields as needed
        }


    def __str__(self):
        return self.name
   
    def save(self, *args, **kwargs):
    # """
    # save price as per margin
    # :param args:
    # :param kwargs:
    # :return:
    # """
        if int(self.quantity) >= 1:
            self.in_stock = True
            self.status = True

        if int(self.quantity) < 1:
            self.in_stock = False
            self.status = False

        super().save(*args, **kwargs)


class AllModels(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=None)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True,blank=True,default=None)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)


class CustomGamingPc(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='categories',default=None)
    product = models.ManyToManyField(Product,related_name='products',max_length=3)
    price = models.IntegerField(default=None)
    created_at = models.DateTimeField(auto_now=True)