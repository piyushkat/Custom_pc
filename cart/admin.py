from django.contrib import admin
from cart.models import CheckoutCart
# Register your models here.
class CheckoutAdmin(admin.ModelAdmin):
    fields = ['cart','user','quantity','custom_gaming_pc','sub_total','shipping','total']
    list_display = ('user','quantity','sub_total','shipping','total','created_at')
admin.site.register(CheckoutCart,CheckoutAdmin)