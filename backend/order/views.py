from urllib import response
from django.http import JsonResponse
from typing import OrderedDict
from django.shortcuts import render
from django.views import generic

from .models import Order,OrderItem
from shop.models import Item

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class CartView(LoginRequiredMixin,generic.ListView):
    login_url = 'accounts/login/'
    redirect_field_name = 'redirect_to'
    model = OrderItem
    template_name = "shop/cart.html"
    context_object_name = 'item_list'
    def get_context_data(self,**kwargs):
        context = super(CartView,self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        if Order.objects.isCart(user=self.request.user):
            order = Order.objects.getOrder(self.request.user)
            return OrderItem.objects.list_carted_items(order=order)
        return None
@login_required
def add_cart(request):
    print("request.get : ",request.GET)

    item_id = request.GET["item_id"]
    item = Item.objects.get(id=item_id)
    item_qty = request.GET["item_qty"]

    # Order which has status =1 and User = request.user is not then create order entry
    if Order.objects.isCart(user=request.user):
        order = Order.objects.getOrder(user = request.user)
    else:
        order = Order(user=request.user,status=1)
        order.save()

    # order exists then update quantity
    if OrderItem.objects.isUpdate(item=item,order=order):
        order_item = OrderItem.objects.get(item=item,order=order)
        order_item.quantity += int(item_qty)
        order_item.save()
    else:
        # create order_item
        order_item = OrderItem(item=item,quantity=item_qty,order=order)
        order_item.save()
    item_count = OrderItem.objects.count_carted_items(order=order)

    res = "Item has been added in the cart."
    return JsonResponse({'data': res, 'carted_item':item_count})

@login_required
def remove_item(request):
    print(request.GET)
    # get item_id from request
    item_id = request.GET["item_id"]
    item = Item.objects.get(id=item_id)
    # get OrderItem entry from item_id and request.user
    order_item = OrderItem.objects.getOrderItem(item=item,user=request.user)
    # delete OrderItem entry
    order_item.delete()
    # return result text and item_count
    item_count = Order.objects.countOrderItem(user=request.user)
    res = "order Item has been deleted."
    return JsonResponse( {'data': res , 'carted_item': item_count} )
    