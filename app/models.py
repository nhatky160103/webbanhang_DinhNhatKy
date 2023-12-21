from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your models here.
class CreateUserForm(UserCreationForm):
    class Meta:
        model =User
        fields=['username','email','first_name','last_name','password1','password2']

class loginUserForm(UserCreationForm):
    class Meta:
        model =User
        fields=['username','password1']

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.SET_NULL, null= True,blank=False)
#     name = models.CharField( max_length=200, null = True)
#     email = models.CharField( max_length=200, null = True)
    
#     def __str__(self) :
#         return self.name



class Category(models.Model):
    sub_category= models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub= models.BooleanField(default=False)
    name= models.CharField(max_length=200, null=True)
    slug= models.SlugField(max_length=200, unique=True)
    def  __str__(self):
        return self.name

class Product(models.Model):
    category= models.ManyToManyField( Category, related_name='product')
    name = models.CharField( max_length=200  , null = True)
    price = models.FloatField()
    shoe_type=models.CharField( max_length=50  , null = True)
    is_shoe = models.BooleanField(default= False, null= True,blank= False)
    image = models.ImageField(null= True,blank=True)
    detail= models.TextField(null=True, blank=True)
    def __str__(self) :
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url
# class Variant(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     color = models.CharField(max_length=50)
#     size = models.CharField(max_length=10)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

class Order(models.Model):
    @property
    def get_cart_items(self):#tính số lượng mặt hàng của người mua (tính tất cả các mặt hàng)
        orderitems = self.orderitem_set.all()
        total= sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):#tính tổng tiền của một đơn hàng
        orderitems = self.orderitem_set.all()
        total= sum([item.get_total for item in orderitems])
        return total
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank= True, null= True)
    date_order=models.DateTimeField( auto_now_add=True)
    complete= models.BooleanField(default=False, null= True,blank= False)
    transaction_id = models.CharField(max_length=200 , null=True)
    def __str__(self) :
        return str(self.id)
    
class OrderItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank= True, null= True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank= True, null= True)
    date_order=models.DateTimeField( auto_now_add=True)
    quantity = models.IntegerField(default= 0, null= True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):# tính tổng tiền của một loạt mặt hàng
        total = self.product.price *self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank= True, null= True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank= True, null= True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    street = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    apartment = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
            return self.address
