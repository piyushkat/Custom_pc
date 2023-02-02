from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from gaming_products.serializer import *
from gaming_products.models import *
import datetime
from authenticate.renderer import UserRenderer
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

class AddCategory(GenericAPIView):
  serializer_class = CategorySerializer
  renderer_classes = [UserRenderer]
  def post(self,request):
    try:
        if not self.request.user.is_authenticated:
          return Response({'msg':'user not found'})
        name = request.data.get('name')
        category = Category.objects.create(user=self.request.user,name=name,created_at=datetime.datetime.now())
        category.save()
        serializer = CategorySerializer(category)
        return Response({"status": "success", "data": serializer.data}, status = 200)
    except:
        return Response({'msg':'Not Added','status':400})


class GetAllCategory(GenericAPIView):
  """
  :return: Get all the category from the category table.
  """
  serializer_class = CategorySerializer
  renderer_classes = [UserRenderer]
  def get(self, request):
      items = Category.objects.all()
      serializer = CategorySerializer(items, many=True)
      return Response({"status": "success", "data": serializer.data}, status = 200)


class AddSubCategory(GenericAPIView):
  serializer_class = SubCategorySeriaizer
  renderer_classes = [UserRenderer]
  def post(self,request):
    try:
        serializer = SubCategorySeriaizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status = 200)
    except:
        return Response({'msg':'Not Added','status':400})


class GetSubCategory(GenericAPIView):
  serializer_class = SubCategorySeriaizer
  renderer_classes = [UserRenderer]
  def get(self,request):
    items = SubCategory.objects.all()
    serializer = SubCategorySeriaizer(items,many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class AddProduct(GenericAPIView):
  serializer_class = ProductSerializer
  renderer_classes = UserRenderer
  def post(self,request):
    try:
      if not self.request.user.is_authenticated:
        return Response({'msg':'user not found'})
      name = request.data.get('name')
      description = request.data.get('description')
      quantity = request.data.get('quantity')
      price = request.data.get('price')
      category = Category.objects.filter(id=request.data['category']).first()
      subcategory = SubCategory.objects.filter(category=category,id=request.data['subcategory']).first()
      product = Product.objects.create(user=self.request.user,name=name,description=description,subcategory=subcategory,category=category,quantity=quantity,price=price)
      product.save()
      serializer = ProductSerializer(product)
      return Response({'msg':'success','data':serializer.data},status=200)
    except:
      return Response({"status": "Not found "}, status = 400)


class GetAllProduct(GenericAPIView):
  serializer_class = ProductSerializer
  renderer_classes = [UserRenderer]
  def get(self,request):
    items = Product.objects.all()
    serializer = ProductSerializer(items,many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class GetProductByCategory(GenericAPIView):
  """
  :return: All the product shown by the category.
  """
  serializer_class = ProductSerializer
  renderer_classes = [UserRenderer]
  def get(self,request,id):
    try:
      res = Product.objects.filter(category=id)
      serializer =  ProductSerializer(res, many=True)
      return Response({"status": "success", "data": serializer.data}, status = 200)
    except:
      return Response({"status": "Not Found"}, status = 400)


class GetProductBySubcategory(GenericAPIView):
  serializer_class = ProductSerializer
  renderer_classes = [UserRenderer]
  def get(self,request,id):
    if not self.request.user.is_authenticated:
      return Response({'msg':'User Not Found'})
    items = Product.objects.filter(subcategory=id)
    serializer = ProductSerializer(items,many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class GetCatSubPro(GenericAPIView):
  serializer_class = AllModelSerializer
  renderer_classes = [UserRenderer]
  def post(self,request,id):
    try:
      if not self.request.user.is_authenticated:
        return Response({'msg':'user not found'})
      category = Category.objects.get(id=id)
      sub_category = SubCategory.objects.filter(category=category,id=request.data['sub_category']).first()
      product = Product.objects.filter(category=category,subcategory=sub_category,id=request.data['product']).first()
      res = AllModels.objects.create(user=self.request.user,category=category,subcategory=sub_category,product=product)
      res.save()
      serializer = AllModelSerializer(res)
      return Response({"status": "success", "data": serializer.data}, status = 200)
    except:
      return Response({"status": "Not found "}, status = 400)


class GetAllModel(GenericAPIView):
  serializer_class = AllModelSerializer
  renderer_classes = [UserRenderer]
  def get(self,request):
    if not self.request.user.is_authenticated:
      return Response({'msg':'User Not Found'})
    order = AllModels.objects.filter(user=self.request.user)
    serializer = AllModelSerializer(order,many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


# class AddProductByCategory(GenericAPIView):
#   def get(self,request,id):
#     try:
#       if not self.request.user.is_authenticated:
#         return Response({'msg':'user not found'})
#       category = Category.objects.get(id=id)
#       product = Product.objects.filter(category=category,id=request.data['product']).first()
#       res = AllModels.objects.create(user=self.request.user,category=category,product=product)
#       res.save()
#       serializer = AllModelSerializer(res)
#       return Response({'msg':'Success','data':serializer.data},status=200)
#     except:
#       return Response({"status": "Not found "}, status = 400)