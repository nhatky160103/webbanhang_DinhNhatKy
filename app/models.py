from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.conf import settings
from django.contrib import admin

from django import forms
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name','password1',  'password2']
        
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg'}),
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
        }
     
        
class loginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']






class Color(models.Model):
    name = models.CharField(max_length=50)
    color_id = models.CharField(max_length=7, default="#000000")
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='product')
    name = models.CharField(max_length=200, null=True)
    price_avg = models.DecimalField(default=0.0,max_digits=10, decimal_places=2)
    shoe_type = models.CharField(max_length=50, null=True)
    is_slider_product = models.BooleanField(default=False, null=True, blank=False)
    detail = models.TextField(null=True, blank=True)
    image = models.ImageField(null= True,blank=True)
    def __str__(self):
        return f"{self.name} - {self.price_avg}"
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url

class ProductVariant(models.Model):
    name = models.CharField(max_length=200, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.0,max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.product.name}" if self.name else "Unnamed Product Variant"
    @property
    def ImageURL(self):
        try:
            url= self.image.url
        except:
            url=''
        return url


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    productvariant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"({self.productvariant}) x {self.quantity}" if self.quantity>0 else "Unnamed OderItem"
    @property
    def get_total(self):
        total = self.productvariant.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    street = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    apartment = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    email= models.EmailField(max_length=200,null=True)
    def __str__(self):
        return self.address


