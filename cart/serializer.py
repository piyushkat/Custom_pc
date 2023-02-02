from rest_framework import serializers
from cart.models import CheckoutCart

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutCart
        fields = ['cart','user','quantity','sub_total','shipping','total']