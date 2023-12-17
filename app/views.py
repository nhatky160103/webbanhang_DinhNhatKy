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
        categories = Category.objects.filter(is_sub= False)
        active_category= request.GET.get('category','')
        user_not_login = "show"
        user_login= "none"
        return render(request, 'app/register.html', {'user_not_login':user_not_login,'user_login':user_login,'categories':categories, 'active_category':active_category,'rF': rF})

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
            categories = Category.objects.filter(is_sub= False)
            active_category= request.GET.get('category','')
            user_not_login = "show"
            user_login= "none"
            return render(request, 'app/register.html', {'user_not_login':user_not_login,'user_login':user_login,'categories':categories, 'active_category':active_category,'rF': rF})

class loginUser(View):
   
    def get(self, request):
        user_not_login = "show"
        user_login= "none"
        lF=loginUserForm()
        categories = Category.objects.filter(is_sub= False)
        active_category= request.GET.get('category','')
        return render(request,'app/login.html',{'categories':categories, 'active_category':active_category,'lF':lF,'user_not_login':user_not_login,'user_login':user_login})
    
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
   
    if request.method =="POST":
        search_id= request.POST["search_id"]
        keys= Product.objects.filter(name__contains = search_id)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete= False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
        user_not_login = "none"
        user_login= "show"

    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
        user_not_login = "show"
        user_login= "none"
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category','')
    context= {'categories':categories, 'active_category':active_category,'products': products, 'cartItems':cartItems,"search_id": search_id, "keys": keys, 'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/search.html',context)


def category(request):
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete= False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
        user_not_login = "none"
        user_login= "show"
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
        user_not_login = "show"
        user_login= "none"
    context= {'categories':categories, 'active_category':active_category, 'cartItems':cartItems,'products':products , 'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/category.html',context)
    



def logout_page(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete= False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
        user_not_login = "none"
        user_login= "show"
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
        user_not_login = "show"
        user_login= "none"
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category', '')
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category','')
    context= {'categories':categories, 'active_category':active_category,'categories':categories,'active_category':active_category,'products':products, 'cartItems':cartItems, 'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete= False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
        user_not_login = "none"
        user_login= "show"
    else:
        items = []
        cartItems=[]
        order = {'get_cart_items':0, 'get_cart_total':0}
        user_not_login = "show"
        user_login= "none"
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category','')
    context= {'categories':categories, 'active_category':active_category,'items':items,'order':order, 'cartItems':cartItems, 'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete= False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
        user_not_login = "none"
        user_login= "show"
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        user_not_login = "show"
        user_login= "none"
        
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category','')
    context= {'categories':categories, 'active_category':active_category,'items':items,'order':order,'cartItems':cartItems, 'user_not_login':user_not_login,'user_login':user_login}#tao mot tu dien den html
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


def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete= False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
        user_not_login = "none"
        user_login= "show"
    else:
        items = []
        cartItems=[]
        order = {'get_cart_items':0, 'get_cart_total':0}
        user_not_login = "show"
        user_login= "none"
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category','')
    context= {'products':products,'categories':categories, 'active_category':active_category,'items':items,'order':order, 'cartItems':cartItems, 'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/detail.html',context)
