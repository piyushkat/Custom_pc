from django.urls import path
from cart.views import *

urlpatterns = [
    path('getcheckoutcart',GetCheckoutCart.as_view(), name='getcheckoutcart'),

]
