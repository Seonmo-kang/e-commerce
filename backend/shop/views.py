from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import generic 

from .models import Brand, Carasel, Category, Item, SubCategory
from order.models import Order, OrderItem
from django.conf import settings




class ShopView(generic.ListView):
    model = Item
    template_name = "shop/shop.html"
    context_object_name = 'item_list'
    
    # def get(self,request, *args, **kwargs):
    #     if request.user.is_authenticated:
            
    #     else:

    def get_context_data(self, **kwargs):
        context = super(ShopView,self).get_context_data(**kwargs)
        # Count cart items function is moved to context_processors.py 
        #   b/c this is not working on extended template.
        # if self.request.user.is_authenticated:
        #     user_order = Order.objects.isCart(user=self.request.user)
        #     count_items = OrderItem.objects.count_carted_items(order=user_order)
        #     context['carted_item'] = count_items #ordered_items
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
        return queryset
        #filter
        # filters={}
        # print(self.request.GET) # Value inspection
        # # for loop in request.GET.items() = query parameters
        # for key, value in self.request.GET.items():
        #     if key in ['category[]','subcategory[]','brand[]']:
        #         print(len(self.request.GET.getlist(key))) # Value inspection
        #         if(len(self.request.GET.getlist(key))>1):
        #             print("key is {0}",key[0:-2])
        #             filters[key[0:-2]+"__name__in"]=self.request.GET.getlist(key)
        #         else:
        #             print("key is {0}",key[0:-2])
        #             filters[key[0:-2]+"__name"]=self.request.GET[key]
        # print(filters) # Value inspection
        # r_string = render_to_string()
        # {queryset.filter(**filters)}
        # return queryset.filter(**filters)
        

def filter_list(request):
    queryset = Item.objects.isAvailable()
    #filter
    filters={}
    print(request.GET) # Value inspection
    # for loop in request.GET.items() = query parameters
    for key, value in request.GET.items():
        if key in ['category[]','subcategory[]','brand[]']:
            print(len(request.GET.getlist(key))) # Value inspection
            if(len(request.GET.getlist(key))>1):
                print("key is ",key[0:-2])
                filters[key[0:-2]+"__name__in"]=request.GET.getlist(key)
            else:
                print("key is ",key[0:-2])
                filters[key[0:-2]+"__name"]=request.GET[key]
    print(filters) # Value inspection
    
    filtered_queryset = queryset.filter(**filters).order_by('-created_at') # queryset
    print("filtered list :",filtered_queryset)

    filtered_list = render_to_string('shop/filtered_list.html',{'item_list': filtered_queryset})
    # print("r_string is ",filtered_list)
    return JsonResponse({'data':filtered_list})


class ItemDetailView(generic.DetailView):
    model = Item
    template_name = "shop/itemDetail.html"
    context_object_name = 'details'
    
    def get_object(self,queryset=None):
        return Item.objects.detail(id=self.kwargs['pk'])

