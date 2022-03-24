from django.views import generic 

from .models import Brand, Carasel, Category, Item, SubCategory
from django.conf import settings

class ShopView(generic.ListView):
    model = Item
    template_name = "shop/shop.html"
    context_object_name = 'item_list'
    

    def get_context_data(self, **kwargs):
        context = super(ShopView,self).get_context_data(**kwargs)

        category = Category.objects.all()
        subcategory = SubCategory.objects.all()
        brand = Brand.objects.all()
        images = Carasel.objects.all()

        context['category'] =category
        context['subcategory'] = subcategory
        context['brand'] = brand
        context['images'] = images
        context['media_url'] = settings.MEDIA_URL
        context['text']= 'This is context[text] context value.'
        return context
    
    # get_query_set will be returned to context_object_name which is 'item_list'
    # Using GET parameter, create dynamic filters.
    def get_queryset(self):
        queryset = Item.objects.isAvailable()
        #filter
        filters={}
        print(self.request.GET) # Value inspection
        # for loop in request.GET.items() = query parameters
        for key, value in self.request.GET.items():
            if key in ['category','subcategory','brand']:
                print(len(self.request.GET.getlist(key))) # Value inspection
                if(len(self.request.GET.getlist(key))>1):
                    filters[key+"__name__in"]=self.request.GET.getlist(key)
                else:
                    filters[key+"__name"]=self.request.GET[key]
        print(filters) # Value inspection
        return queryset.filter(**filters)


    
class ItemDetailView(generic.DetailView):
    model = Item
    template_name = "shop/itemDetail.html"
    context_object_name = 'details'
    
    def get_object(self,queryset=None):
        return Item.objects.detail(id=self.kwargs['pk'])

class ItemFilterView(ShopView):

    def get_context_data(self, **kwargs):
        context = super(ItemFilterView,self).get_context_data(**kwargs)
        #test code
        # context['category'] =category
        # context['subcategory'] =subcategory
        # context['brand'] =brand
        print(self.kwargs)
        for key,value in self.kwargs.items():
            if(value==''):
                self.kwargs.pop(key)
            # print(key)
            # print(value)
        print(self.kwargs)
        # print(brand)
        # print(category)
        # print(subcategory)

        itemlist = Item.objects.itemList()
        # category=category,subcategory=subcategory,brand=brand
        images = Carasel.objects.all()

        context['images'] = images
        context['media_url'] = settings.MEDIA_URL
        context['item'] = itemlist
        context['text']= 'This is context[text] context value.'
        return context

