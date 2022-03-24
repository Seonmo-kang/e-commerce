from django.urls import path, re_path, include
from .views import ItemDetailView, ShopView, ItemFilterView
urlpatterns = [
    path('',ShopView.as_view(),name='shopHomePage'),
    path(r'item/<int:pk>',ItemDetailView.as_view(),name='ItemDetailPage'),
    # itemlist filter using regex
   re_path(r'^itemlist/(?P<category>[\w]*)/(?P<subcategory>[\w]*)/(?P<brand>[\w]*)/$'
   ,ItemFilterView.as_view(),name='ItemFilterView'),
   # itemlist filter using query
#    path(r'itemlist/')
]