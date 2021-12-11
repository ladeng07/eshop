from django.contrib import admin
from app1.models import *


# Register your models here.

class CustoomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'password', "email", "money", "sex", "register_time", "status")
    list_editable = ('status',)
    list_per_page = 5
    search_fields = ['name']
    date_hierarchy = 'register_time'
    empty_value_display = 'NA'
    list_filter = ('status', "register_time",)


class SellerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", 'password', "email", "sex", "register_time", "status")
    list_editable = ('status',)
    list_per_page = 5
    search_fields = ['name']
    date_hierarchy = 'register_time'
    empty_value_display = 'NA'
    list_filter = ('status', "register_time",)


class GoodsAdmin(admin.ModelAdmin):
    list_display = (
    "id", "item_name", "item_introduction", "create_time", "number", "item_price", "category_id", "status")
    list_editable = ('status',"category_id")
    list_per_page = 5
    search_fields = ['item_name']
    date_hierarchy = 'create_time'
    empty_value_display = 'NA'
    list_filter = ('status', "create_time","category_id")
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "create_time", "number","address","sum_price","status","buyer_id","item_id")
    list_editable = ('status', "number","address","sum_price",)
    list_per_page = 5
    search_fields = ['address']
    date_hierarchy = 'create_time'
    empty_value_display = 'NA'
    list_filter = ('status', "create_time", )

admin.site.register(Customer, CustoomerAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Order, OrderAdmin)
