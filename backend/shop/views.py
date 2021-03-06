
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import generic 
from django.db.models import F,OuterRef, Exists, Count, Avg, FloatField,Subquery
from .models import Brand, Carasel, Category, Item, ItemImage, SubCategory,Wish, Review
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
        if self.request.user.is_authenticated:
            wish = Wish.objects.get_wishList_or_none(user=self.request.user)
            context['wish_list']=wish
        context['wish_list']=None
        context['category'] =category
        context['subcategory'] = subcategory
        context['brand'] = brand
        context['carousel_images'] = images
        context['media_url'] = settings.MEDIA_URL
        context['text']= 'This is context[text] context value.'
        return context
    
    # get_query_set will be returned to context_object_name which is 'item_list'
    # Using GET parameter, create dynamic filters.
    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Item.objects.isAvailable().annotate(wished_item=Exists(Wish.objects.filter(user=self.request.user,item=OuterRef('pk'))))
        else:
            queryset = Item.objects.isAvailable()
        counts = Subquery(Review.objects.filter(item__id=OuterRef('id')).annotate(counts = Count('id')).values('counts'))
        queryset = queryset.annotate(counts = counts)
        avg = Subquery(Review.objects.filter(item__id=OuterRef('id')).values('item').annotate(avg = Avg('star')).values('avg'))
        queryset = queryset.annotate(avg = avg)
        main_image = Subquery(ItemImage.objects.filter(item__id=OuterRef('id')).values('image')[:1])
        queryset = queryset.annotate(main_image=main_image)
        # queryset.values('item').aggregate(review_avg=Avg(counts),output_field=FloatField())
        print(queryset.query,"\n")
        print(queryset[0].main_image)
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
    main_image = Subquery(ItemImage.objects.filter(item__id=OuterRef('id')).values('image')[:1])
    filtered_queryset = filtered_queryset.annotate(main_image=main_image)
    if request.user.is_authenticated:
        filtered_queryset = filtered_queryset.annotate(wished_item=Exists(Wish.objects.filter(user=request.user,item=OuterRef('pk'))))
    counts = Subquery(Review.objects.filter(item__id=OuterRef('id')).annotate(counts = Count('id')).values('counts'))
    filtered_queryset = filtered_queryset.annotate(counts = counts)
    avg = Subquery(Review.objects.filter(item__id=OuterRef('id')).values('item').annotate(avg = Avg('star')).values('avg'))
    filtered_queryset = filtered_queryset.annotate(avg = avg)
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
    
    def get_context_data(self, **kwargs):
        context = super(ItemDetailView,self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            item = Item.objects.get(id=self.kwargs['pk'])
            context['wish'] = Wish.objects.get_wishItem_or_none(user=self.request.user,item=item)
        context['review_count'] = Review.objects.filter(item__id=self.kwargs['pk']).aggregate(count=Count('item'))
        context['review_avg'] = Review.objects.filter(item__id=self.kwargs['pk']).aggregate(avg = Avg('star'))
        context['review_list'] = Review.objects.filter(item_id=self.kwargs['pk'])
        context['images'] = ItemImage.objects.filter(item_id=self.kwargs['pk'])
        return context