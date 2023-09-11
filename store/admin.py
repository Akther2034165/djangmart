from django.contrib.admin import ModelAdmin
from django.contrib import admin
from .models import Product
# Register your models here.


class ProductAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'price','stock','category', 'modified_date', 'is_available',)

admin.site.register(Product, ProductAdmin)