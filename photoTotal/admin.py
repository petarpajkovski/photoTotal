from django.contrib import admin
from . import models


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'brand', 'name', 'price', 'quantity']
    list_filter = ['category', 'brand']
    list_editable = ['price', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['costumer', 'date_ordered', 'transaction_id', 'complete']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity']


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.ShippingAddress)
