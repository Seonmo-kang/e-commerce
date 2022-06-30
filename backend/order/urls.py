from django.urls import path,re_path,include
from .views import CartView, add_cart, remove_item, manage_wish, WishView

urlpatterns =[
    path('cart/', CartView.as_view() , name='cart'),
    path('addCart/', add_cart, name='addCart'),
    path('remove_item/',remove_item, name ='removeItem'),
    path('manageWish/',manage_wish,name='addWish'),
    path('wishList/',WishView.as_view(), name='wish_list'),
]