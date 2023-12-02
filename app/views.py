from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
class registerUser(View):
    def get(self, request):
        rF = CreateUserForm()
        return render(request, 'app/register.html', {'rF': rF})

    def post(self, request):
        rF = CreateUserForm(request.POST)
        if rF.is_valid():
            username = rF.cleaned_data['username']
            password = rF.cleaned_data['password1']
            email = rF.cleaned_data.get('email')
            
            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = rF.cleaned_data.get('first_name')
            user.last_name = rF.cleaned_data.get('last_name')
            user.save()
            return redirect('login')
        else:
            return render(request, 'app/register.html', {'rF': rF})

class loginUser(View):
    def get(self, request):
        lF=loginUserForm()
        return render(request,'app/login.html',{'lF':lF})
    
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        username=  request.POST['username']
        password=request.POST['password']
        user= authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'Username or password is incorrect')
            return render(request, 'app/login.html', {'lF': loginUserForm()})
           
def search(request):
    return render(request, 'app/search.html')

def logout_page(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete= False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
    products = Product.objects.all()
    context= {'products': products, 'cartItems':cartItems}
    return render(request,'app/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete= False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
    context= {'items':items,'order':order, 'cartItems':cartItems}
    return render(request,'app/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete= False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}

    context= {'items':items,'order':order,'cartItems':cartItems}#tao mot tu dien den html
    return render(request,'app/checkout.html',context)
def updateItem(request):
    data =json.loads(request.body)
    productId =data['productId']
    action = data['action']
    customer = request.user
    product=Product.objects.get(id= productId)
    order, created = Order.objects.get_or_create(customer = customer,complete= False)
    orderItem, created = OrderItem.objects.get_or_create(order = order,product= product)
    if action=='add':
        orderItem.quantity+=1
    elif action=='remove':
        orderItem.quantity-=1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    
    return JsonResponse('added',safe=False)