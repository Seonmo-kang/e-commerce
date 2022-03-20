

from django.views import generic 

from .models import Carasel, Item
from django.conf import settings

class ShopView(generic.ListView):
    model = Item
    template_name = "shop/shop.html"
    context_object_name = 'item_list'
    

    def get_context_data(self, **kwargs):
        context = super(ShopView,self).get_context_data(**kwargs)
        itemlist = Item.objects.isAvailable()
        images = Carasel.objects.all()

        context['images'] = images
        context['media_url'] = settings.MEDIA_URL
        context['item'] = itemlist
        context['text']= 'This is context[text] context value.'
        return context

    # *** in def get_query_set,
    # if you want to use model Manager, then you should use self.model parameter in queryset
    def get_queryset(self):
        return Item.objects.isAvailable()
    
        
