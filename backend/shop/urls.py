from django.urls import path, re_path, include
from .views import ItemDetailView, ShopView, filter_list
urlpatterns = [
    path('',ShopView.as_view(),name='shopHomePage'),
    path(r'filter-list/',filter_list,name='filter list'),
    path(r'item/<int:pk>',ItemDetailView.as_view(),name='ItemDetailPage'),
    # itemlist filter using regex
#    re_path(r'^itemlist/(?P<category>[\w]*)/(?P<subcategory>[\w]*)/(?P<brand>[\w]*)/$'
#    ,ItemFilterView.as_view(),name='ItemFilterView'),
# itemlist filter using query
#    path(r'itemlist/')
]