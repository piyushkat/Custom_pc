from django.shortcuts import render
from cart.models import CheckoutCart
from cart.serializer import CheckoutSerializer,CustomGamingPcCheckoutSerializer
from authenticate.renderer import UserRenderer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from gaming_products.models import AllModels
from gaming_products.models import CustomGamingPc
# Create your views here.

class GetCheckoutCart(GenericAPIView):
    serializer_class = CheckoutSerializer
    renderer_classes = [UserRenderer]
    def post(self, request):
        if not self.request.user.is_authenticated:
            return Response({'msg':'User Not Found'})
        cart_items = AllModels.objects.filter(user=self.request.user)
        sub_total = 0
        quantities = 0
        shipping_cost = 3520
        for cart_item in cart_items:
            sub_total += cart_item.quantity * cart_item.product.price
            quantities += cart_item.quantity
        total = sub_total + shipping_cost
        cart_values = CheckoutCart.objects.create(
            user=self.request.user,
            quantity=quantities,
            shipping=shipping_cost,
            sub_total=sub_total,
            total=total
        )
        cart_values.cart.set(cart_items)
        cart_values.save()
        serializer = CheckoutSerializer(cart_values)
        return Response({"status": "success", "data": serializer.data}, status=200)


class CustomGamingCart(GenericAPIView):
    serializer_class = CustomGamingPcCheckoutSerializer
    def post(self,request):
        if not self.request.user.is_authenticated:
            return Response({'msg':'User Not Found'})
        custom_gaming = CustomGamingPc.objects.filter(user=self.request.user)
        shipping_cost = 3520
        total = sum(item.price for item in custom_gaming)
        totals = total+shipping_cost
        cart_values = CheckoutCart.objects.create(user=self.request.user, shipping=shipping_cost, total=totals)
        cart_values.custom_gaming_pc.set(custom_gaming)
        cart_values.save()
        serializer = CustomGamingPcCheckoutSerializer(cart_values,many=True)
        return Response({'msg':'Success','data':serializer.data},status=200)