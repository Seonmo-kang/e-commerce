from csv import list_dialects
from re import search
from django.contrib import admin
from .models import Item,Qty,Category,SubCategory,Brand,Review, Carasel, Wish
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id','name','description','sell_price',
    'unit_price','code','model','color','isAvailable']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class QtyAdmin(admin.ModelAdmin):
    list_display = ['id','item','qty_on_hand','qty_on_purchase',
                    'qty_in_transit','qty_on_sold','qty_in_cancel']
    # fieldsets =[
    #      ('Information',{'fields':('id','item')}),
    #      ('Qty',{'fields':('qty_on_hand','qty_on_purchase',
    #                  'qty_in_transit','qty_on_sold','qty_in_cancel')})
    # ]
    search_fields = ('item',)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'user', 'star', 'subject', 'context']

class CaraselAdmin(admin.ModelAdmin):
    list_display = ['alt','image']

class WishAdmin(admin.ModelAdmin):
    list_display= ['id','user','item']

admin.site.register(Item,ItemAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Qty,QtyAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Carasel,CaraselAdmin)
admin.site.register(Wish,WishAdmin)
