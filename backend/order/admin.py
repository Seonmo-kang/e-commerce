from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress

class OrderAdmin(admin.ModelAdmin):
    display_list = ['transit_id', 'status','user']

class OrderItemAdmin(admin.ModelAdmin):
    display_list = ['orderitem_id', 'item', 'order', 'quantity']

class ShippingAddressAdmin(admin.ModelAdmin):
    display_list = ['address_id', 'user', 'order', 'address', 'city', 'state', 'zipcode']

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(ShippingAddress,ShippingAddressAdmin)
