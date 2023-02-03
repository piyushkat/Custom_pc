from django.urls import path
from gaming_products.views import *

urlpatterns = [
    path('getcat/<int:id>',GetCatSubPro.as_view(), name='getcat'),
    path('getproductbycategory/<int:id>',GetProductByCategory.as_view(), name='getproductbycategory'),
    path('addcategory',AddCategory.as_view(), name='addcategory'),
    path('addproduct',AddProduct.as_view(), name='addproduct'),
    path('getallcategory',GetAllCategory.as_view(), name='getallcategory'),
    path('addsub',AddSubCategory.as_view(), name='addsub'),
    path('getsubcategory',GetSubCategory.as_view(), name='getsubcategory'),
    path('getproductbysubcategory/<int:id>',GetProductBySubcategory.as_view(), name='getproductbysubcategory'),
    path('getallproduct',GetAllProduct.as_view(), name='getallproduct'),
    path('getbyuser',GetAllModel.as_view(), name='getbyuser'),
    path('customgaming/<int:id>',CreateCustomGamingPc.as_view(), name='customgaming'),
    # path('getcustomgaming',GetCustomGamingPc.as_view(), name='getcustomgaming'),
    # path('addproductbycategory/<int:id>',AddProductByCategory.as_view(), name='getbyuser'),

]
