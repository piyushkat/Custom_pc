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
    if not self.request.user.is_authenticated:
      return Response({'msg':'user not found'})
    name = request.data.get('name')
    category = Category.objects.get(id=request.data['category'])
    sub_category = SubCategory.objects.create(user=self.request.user,name=name,category=category)
    sub_category.save()
    serializer = SubCategorySeriaizer(sub_category)
    return Response({"status": "success", "data": serializer.data}, status = 200)



class GetSubCategory(GenericAPIView):
  serializer_class = SubCategorySeriaizer
  renderer_classes = [UserRenderer]
  def get(self,request):
    items = SubCategory.objects.all()
    serializer = SubCategorySeriaizer(items,many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class AddProduct(GenericAPIView):
  def post(self,request):
    if not self.request.user.is_authenticated:
      return Response({'msg':'user not found'})
    print("nfi")
    # try:
    name = request.data.get('name')
    description = request.data.get('description')
    quantity = request.data.get('quantity')
    price = request.data.get('price')
    category = Category.objects.get(id=request.data['category'])
    sub_category = SubCategory.objects.filter(category=category,id=request.data['sub_category']).first()
    product = Product.objects.create(user=self.request.user,name=name,description=description,quantity=quantity,price=price,category=category,subcategory=sub_category)
    product.save()
    serializer = ProductSerializer(product)
    return Response({"status": "success", "data": serializer.data}, status = 200)



class GetAllProduct(GenericAPIView):
  serializer_class = ProductSerializer
  def get(self,request):
    items = Product.objects.all()
    serializer = ProductSerializer(items,many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class GetProductByCategory(GenericAPIView):
  """
  :return: All the product shown by the category.
  """
  serializer_class = ProductSerializer
  def get(self,request,id):
    try:
      res = Product.objects.filter(category=id)
      serializer =  ProductSerializer(res, many=True)
      return Response({"status": "success", "data": serializer.data}, status = 200)
    except:
      return Response({"status": "Not Found"}, status = 400)


class GetProductBySubcategory(GenericAPIView):
  serializer_class = ProductSerializer
  def get(self,request,id):
    if not self.request.user.is_authenticated:
      return Response({'msg':'User Not Found'})
    items = Product.objects.filter(subcategory=id)
    serializer = ProductSerializer(items,many=True)
    return Response({"status": "success", "data": serializer.data}, status = 200)


class GetCatSubPro(GenericAPIView):
  serializer_class = AllModelSerializer
  def post(self,request,id):
    try:
      if not self.request.user.is_authenticated:
        return Response({'msg':'user not found'})
      category = Category.objects.get(id=id)
      quantity = int(request.data['quantity'])
      sub_category = SubCategory.objects.filter(category=category,id=request.data['sub_category']).first()
      product = Product.objects.filter(category=category,subcategory=sub_category,id=request.data['product']).first()
      try:
        res = AllModels.objects.get(user=self.request.user,category=category,subcategory=sub_category,product=product)
        res.quantity += quantity
      except:
        res = AllModels.objects.create(user=self.request.user,category=category,subcategory=sub_category,product=product,quantity=quantity)
      res.save()
      serializer = AllModelSerializer(res)
      return Response({"status": "success", "data": serializer.data}, status = 200)
    except:
      return Response({"status": "Not found "}, status = 400)


class GetAllModel(GenericAPIView):
  serializer_class = AllModelSerializer
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

# class CreateCustomGamingPc(GenericAPIView):
#     serializer_class = CustomGaminPcSerializer
#     renderer_classes = [UserRenderer]
#     def post(self,request,id):
#         category = Category.objects.get(id=id)
#         products = Product.objects.filter(category=category, id=request.data['product'])
#         price = request.data.get('price')
#         res = CustomGamingPc.objects.filter(user=self.request.user,category=category)
#         if res.exists():
#             res = res.first()
#             res.product.add(*products)
#         else:
#             res = CustomGamingPc.objects.create(user=self.request.user,category=category,price=price)
#             res.product.set(products)
#         res.save()
#         serializer = CustomGaminPcSerializer(res)
#         return Response({'msg':'Success','data':serializer.data},status=200)

class CreateCustomGamingPc(GenericAPIView):
    serializer_class = CustomGaminPcSerializer
    renderer_classes = [UserRenderer]
    
    def post(self, request, id):
      id = [id] if not isinstance(id, list) else id
      category = Category.objects.get(id=id[0])
      products = Product.objects.filter(category=category, id__in=request.data['product'])
      price = request.data.get('price')
      if len(products)> 3:
        return Response({'msg':'Only Select Three'})
      else:
        res = CustomGamingPc.objects.filter(user=self.request.user,category=category)
        if res.exists():
            res = res.first()
            res.product.add(*products)
        else:
            res = CustomGamingPc.objects.create(user=self.request.user,category=category,price=price)
            res.product.set(products)
        res.save()
        serializer = CustomGaminPcSerializer(res)
        return Response({'msg':'Success','data':serializer.data},status=200)

class GetCustomGamingPc(GenericAPIView):
  def get(self, request):
    if not request.user.is_authenticated:
        return Response({'msg': 'User not found'})

    custom_game = CustomGamingPc.objects.filter(user=self.request.user).first()
    if custom_game is None:
        return Response({'msg': 'Custom gaming PC not found'})

    products = Product.objects.filter(category=custom_game.category)
    diff = 0
    closest_match = None
    min_diff = float('inf')
    for product in products:
        diff += abs(custom_game.price - product.price)
        if diff <= min_diff:
            closest_match = product
            min_diff = diff

    if closest_match.price == custom_game.price:
        return Response({'msg': 'Success', 'data': closest_match.to_dict()}, status=200)
    else:
        return Response({'msg': 'Success', 'data': closest_match.to_dict()}, status=200)
