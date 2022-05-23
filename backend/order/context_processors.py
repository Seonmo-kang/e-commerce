   # count carted items i all templates
from .models import Order,OrderItem

def cart_processor(request):
    if request.user.is_authenticated and Order.objects.exists():
        user_order = Order.objects.getOrder(user=request.user)
        count_items = OrderItem.objects.count_carted_items(order=user_order)
    else:
        count_items = None
    return {
        'carted_item' : count_items
    }
    # return to base.html -> carted_item