from django.urls import path,re_path,include
from .views import CartView, add_cart, remove_item

urlpatterns =[
    path('cart/', CartView.as_view() , name='cart'),
    path('addCart/', add_cart, name='addCart'),
    path('remove_item/',remove_item, name ='removeItem'),
]