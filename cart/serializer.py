from rest_framework import serializers
from cart.models import CheckoutCart

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutCart
        fields = ['cart','user','quantity','sub_total','custom_gaming_pc','shipping','total']


class CustomGamingPcCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutCart
        fields = ['user','quantity','custom_gaming_pc','shipping','total']