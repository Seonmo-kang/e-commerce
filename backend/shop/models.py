from email.mime import image
from unicodedata import category
from django.db import models
from django.conf import settings
from django.forms import SlugField

from bases.models import TimeStampBase

from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

# Item Category
class Category(TimeStampBase):
    id = models.BigAutoField('Category ID',primary_key=True)
    name = models.CharField('Category Name',max_length=50,unique=True,default='category')
    # slug =  models.SlugField('Category Slug', max_length=50,unique=True)
    def slug(self):
        return slugify(self.name)
    def __str__(self):
        return self.name

# Item SubCategory
class SubCategory(TimeStampBase):
    id = models.BigAutoField('Subcategory ID',primary_key=True)
    name = models.CharField('Subcategory Name',max_length=50,unique=True,default='subcategory')
    slug =  models.SlugField('Subcategory Slug', max_length=50,unique=True)
    # def slug(self):
    #     return slugify(self.name)
    def __str__(self):
        return self.name

class Brand(TimeStampBase):
    id = models.BigAutoField('Brand ID',primary_key=True)
    name = models.CharField('Brand Name', max_length=50,unique=True,default='Brand')
    # slug = models.SlugField('Brand Slug', max_length=50,unique=True)
    def slug(self):
        return slugify(self.name)
    def __str__(self):
        return self.name

# Carasel Model
class Carasel(TimeStampBase):
    alt = models.CharField('Alt name',max_length=50,default="Alt")
    image = models.ImageField(upload_to = 'carasel/') # /static/images/carasel
    def __str__(self):
        return self.alt

# Item Manager model
class ItemManager(models.Manager):
    #Return Item List
    # def itemlist(self,**kwargs):
    #     for key,value in kwargs.items():
    #         if(value=='all'):

        
    #     return self.filter(isAvailable=True,
    #                         category__name=kwargs['category'],
    #                         subcategory__name = kwargs['subcategory'],
    #                         brand__name = kwargs['brand'])
    # Return Item Detail
    def detail(self,**kwargs):
        return self.get(isAvailable=True,**kwargs)
    # Objects have isAvailable=True
    def isAvailable(self, **kwargs):
        return self.filter(isAvailable=True,**kwargs)

    # Objects have mix color
    def mixColor(self,**kwargs):
        return self.filter(color="mix",**kwargs)

    # def get_queryset(self):
    #     return super(ItemManager,self).get_queryset().filter(isAvailable=True)

# Item model
class Item(TimeStampBase):
    """
        id
        name
        description
        sell price
        unit price
        code
        model
        color
        isAvailable
        qty Fk
        category Fk
        subCategory Fk
    --need to be created
        images
    """
    id = models.BigAutoField('Item ID',primary_key=True)
    name = models.CharField('Item Name',max_length=100)
    description = models.CharField('Item Description',max_length=500,blank=True)
    sell_price = models.BigIntegerField('Selling Price',default=1) #판매가
    unit_price = models.BigIntegerField('Unit Price',default=1) #단가
    code = models.CharField('Item Code',max_length=30,unique=True)
    model = models.CharField('Item Model Code',max_length=30,unique=True)
    weight = models.FloatField('Item Weigth',default=0) #제품 무게
    MADE_IN_CHOICES=[
        ('jp','Japan'),
        ('kr','Korea'),
        ('ch','China'),
        ('us','USA')
    ]
    made_in = models.CharField('Made In',max_length=2,choices=MADE_IN_CHOICES,default='ch')#제품 제조국
    COLOR_CHOICE =[
        ('mix','Mix'),
        ('mono','Mono')
    ]
    color = models.CharField(max_length=4, choices=COLOR_CHOICE, default=COLOR_CHOICE)
    isAvailable = models.BooleanField('Is Available', default=False)
    isDiscounted = models.BooleanField('Is Discounted',default=False)
    #FK
    brand = models.ForeignKey(Brand,on_delete=models.PROTECT,related_name='item') #제품 브랜드
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='item') #제품 카테고리
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='item') #제품 카테고리
    
    # Columns - need to be created
    # 이미지는 따로 만들고 만든 이미지 모델에 item을 FK로 추가한다.
    # created_by_who : Auth 처리가 가능할때 만들도록한다.
    # Count 횟수 : Count 횟수 저장한다.

    objects = ItemManager()

    def __str__(self):
        return self.name
class ItemImage(TimeStampBase):
    id = models.BigAutoField("Image ID",primary_key=True)
    item = models.ForeignKey('item',on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'item_images/') # /static/images/item_images

# Item Stock model
class Qty(TimeStampBase):
    id = models.BigAutoField('Qty ID',primary_key=True)
    item = models.OneToOneField(Item,on_delete=models.CASCADE,related_name='qty')
    qty_on_hand = models.IntegerField('Qty on Hand',default=0)
    qty_on_purchase = models.IntegerField('Qty on Purchase',default=0)
    qty_in_transit = models.IntegerField('Qty in Transit',default=0)
    qty_on_sold = models.IntegerField('Qty on Sold',default=0)
    qty_in_cancel = models.IntegerField('Qty in Cancel',default=0)


# #Item Images
# class ItemImage(TimeStampBase):
#     item = models.ForeignObject(Item,on_delete=models.CASCADE,related_name='images')
#     image = 

# Item review model
class Review(TimeStampBase):
    id = models.BigAutoField('Review ID', primary_key=True)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='review')
    STAR_CHOICE=[
        (1,"⭐"),
        (2,"⭐⭐"),
        (3,"⭐⭐⭐"),
        (4,"⭐⭐⭐⭐"),
        (5,"⭐⭐⭐⭐⭐")
    ]
    star = models.IntegerField("Review Star",choices=STAR_CHOICE,default=1)
    subject = models.CharField("Review Subject",max_length=200,null=False,blank=False)
    context = models.TextField("Review Context",null=False,blank=False)
    # Adding reivew photo?

class WishManager(models.Manager):
    # user has wish object?
    def hasWishList(self,user,**kwargs):
        return self.filter(user=user).exists()
    # user has this item in wishlist?
    def isInWishList(self,user,item,**kwargs):
        if self.hasWishList(user=user):
            return self.filter(user=user,item=item).exists()
        return False
    # Get or None wishList
    def get_wishItem_or_none(self,user,item,**kwargs):
        if self.isInWishList(user=user,item=item):
            return self.get(user=user,item=item)
        return None  
    # Get user's wishList querySet or None
    def get_wishList_or_none(self,user,**kwargs):
        if self.hasWishList(user=user):
            return self.filter(user=user)
        return None
class Wish(TimeStampBase):
    id = models.BigAutoField('Wish id', primary_key=True)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='wish')
    objects= WishManager()

    def __str__(self):
        return str(self.user)+" "+str(self.item)

