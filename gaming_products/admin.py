from django.contrib import admin
from gaming_products.models import Category,SubCategory,Product,AllModels
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display= ('id','user','name','created_at','updated_at')
admin.site.register(Category,CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','user','name','category','created_at')
admin.site.register(SubCategory,SubCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','user','name','description','subcategory','category','quantity','in_stock','price','created_at','updated_at')
admin.site.register(Product,ProductAdmin)


class AllModelAdmin(admin.ModelAdmin):
    list_display = ('user','category','subcategory','product','quantity')
admin.site.register(AllModels,AllModelAdmin)