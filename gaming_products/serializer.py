from rest_framework import serializers
from django.contrib.auth.models import User
from gaming_products.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','created_at','updated_at']


class SubCategorySeriaizer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id','user','name','category','created_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','description','quantity','in_stock','category','subcategory','price','created_at','updated_at']


class AllModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllModels
        fields = ['category','subcategory','product']