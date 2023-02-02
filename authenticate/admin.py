from django.contrib import admin
from authenticate.models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email','first_name','last_name','phone_no')
    
admin.site.register(User,UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'auth_token', 'is_verified',
                    'is_admin', 'created_at')
admin.site.register(Profile,ProfileAdmin)