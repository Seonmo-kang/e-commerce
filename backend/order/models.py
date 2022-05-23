from django.db import models
from django.conf import settings

from bases.models import TimeStampBase
from shop.models import Item, Qty

from django.core.validators import RegexValidator
from datetime import datetime
from uuid import uuid4

class OrderManager(models.Manager):
    def getOrder(self,user,**kwargs):
        return self.get(status=1,user=user,**kwargs)
    
    def isCart(self,user,**kwargs):
        return self.filter(status=1, user=user, **kwargs).exists()

    def countOrderItem(self,user,**kwargs):
        try:
            order = self.get(status=1, user=user, **kwargs)
        except order.DoesNotExist:
            return 0
        return OrderItem.objects.count_carted_items(order=order)
    # def isOrdered
    # def isCancelled
# Order
class Order(TimeStampBase):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    transit_id = models.CharField(primary_key=True,max_length=20)

    COMPLETE_CHOICE =(
        (1,'Cart'),
        (2,'Ordered'),
        (3,'In Transit'),
        (4,'Completed'),
        (5,'Cancelled')
    )
    status = models.SmallIntegerField('Order Status',choices=COMPLETE_CHOICE,default=1)

    objects = OrderManager()

    def create_id(self):
        now = datetime.now()
        return str(now.year)+str(now.month)+str(now.day)+str(uuid4())[:7]
    def save(self):
        if not self.transit_id:
            self.transit_id = self.create_id()
            while Order.objects.filter(transit_id=self.transit_id).exists():
                self.transit_id = self.create_id()
        return super(Order, self).save()
    def __str__(self):
        return str(self.transit_id)

class OrderItemManager(models.Manager):
    def getOrderItem(self,item,user,**kwargs):
        if Order.objects.isCart(user=user):
            order = Order.objects.getOrder(user=user)
            print("order is on the order DB.")
            return self.get(order=order,item=item)
        return None
    def isUpdate(self,item,order,**kwargs):
        return self.filter(item=item,order=order).exists()

    def count_carted_items(self,order,**kwargs):
        return self.filter(order=order).count()

    def list_carted_items(self,order,**kwargs):
        return self.filter(order=order)
# Items in Order
class OrderItem(TimeStampBase):
    orderItem_id = models.BigAutoField('Order Item Id',primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE,null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.SmallIntegerField('Order Qty',default=0)

    objects = OrderItemManager()

# Order shipping address
class ShippingAddress(TimeStampBase):
    address_id = models.BigAutoField('Address Id',primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200, null=True)
    city =models.CharField(max_length=30,null=True,blank=True)
    STATE_CHOICES=(
    ('AL','Alabama'),('AK','Alaska'),('AZ','Arizona'),('AR','Arkansas'),('CA','California'),('CO','Colorado'),('CT','Connecticut'),('DE','Delaware'),('FL','Florida'),('GA','Georgia'),('HI','Hawaii'),('ID','Idaho'),('IL','Illinois'),('IN','Indiana'),('IA','Iowa'),('KS','Kansas'),('KY','Kentucky'),('LA','Louisiana'),('ME','Maine'),('MD','Maryland'),('MA','Massachusetts'),('MI','Michigan'),('MN','Minnesota'),('MS','Mississippi'),('MO','Missouri'),('MT','Montana'),('NE','Nebraska'),('NA','Nevada'),('NH','New Hampshire'),('NJ','New Jersey'),('NM','New Mexico'),('NY','New York'),('NC','North Carolina'),('ND','North Dakota'),('OH','Ohio'),('OK','Oklahoma'),('OR','Oregon'),('PA','Pennsylvania'),('RI','Rhode Island'),('SC','South Carolina'),('SD','South Dakota'),('TN','Tennessee'),('TX','Texas'),('UT','Utah'),('VT','Vermont'),('VA','Virginia'),('WA','Washington'),('WV','West Virginia'),('WI','Wisconsin'),('WY','Wyoming')
    )
    state = models.CharField(max_length=2,choices=STATE_CHOICES,default=STATE_CHOICES)
    zipcodeValidator = RegexValidator(r"^([0-9]{5}(?:-[0-9]{4})?$)",r"Error: Must be Digit 5 E.g. 00000 or 00000-0000")
    zipcode = models.CharField(max_length=12,validators=[zipcodeValidator],blank=True,null=True)







