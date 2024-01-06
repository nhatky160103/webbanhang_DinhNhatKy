from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.views import APIView
from .serializer import GetAllProductvariant
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
class registerUser(View):
    def get(self, request):
        rF = CreateUserForm()
        categories = Category.objects.filter(is_sub= False)
        active_category= request.GET.get('category','')
        return render(request, 'app/register.html', {'categories':categories, 'active_category':active_category,'rF': rF})

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
            return render(request, 'app/register.html', {'categories':categories, 'active_category':active_category,'rF': rF})

class loginUser(View):
   
    def get(self, request):
        lF=loginUserForm()
        categories = Category.objects.filter(is_sub= False)
        active_category= request.GET.get('category','')
        return render(request,'app/login.html',{'categories':categories, 'active_category':active_category,'lF':lF})
    
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

    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category','')
    context= {'categories':categories, 'active_category':active_category,'products': products, 'cartItems':cartItems,"search_id": search_id, "keys": keys}
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
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
    context= {'categories':categories, 'active_category':active_category, 'cartItems':cartItems,'products':products }
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
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems= order['get_cart_items']
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category', '')
    products = Product.objects.all()
    products_slider= Product.objects.filter(is_slider_product= True)
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category','')
    context= {'categories':categories, 'active_category':active_category,'categories':categories,'active_category':active_category,'products':products, 'cartItems':cartItems,'products_slider':products_slider}
    return render(request,'app/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete= False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        items = []
        cartItems=[]
        order = {'get_cart_items':0, 'get_cart_total':0}
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category','')
    context= {'categories':categories, 'active_category':active_category,'items':items,'order':order, 'cartItems':cartItems}
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
        return redirect('login')
        
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category','')
    context= {'categories':categories, 'active_category':active_category,'items':items,'order':order,'cartItems':cartItems}#tao mot tu dien den html
    return render(request,'app/checkout.html',context)


def save_shipping_address(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete= False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            city = request.POST.get('city')
            street = request.POST.get('street')
            apartment = request.POST.get('apartment')
            phone_number = request.POST.get('phone_number')

            shipping_address = ShippingAddress(
                customer=customer,
                address=address,
                email= email,
                order= order,
                city=city,
                street=street,
                apartment=apartment,
                phone_number=phone_number
            )
            shipping_address.save()
            return redirect('checkout')
    else:
        items = []
        cartItems=[]
        order = {'get_cart_items':0, 'get_cart_total':0}
        return redirect("login")
   
   





def updateItem(request):
    data =json.loads(request.body)
    productvariant_id =data['productvariant_id']
    action = data['action']
    customer = request.user
    productvariant=ProductVariant.objects.get(id= productvariant_id)
    order, created = Order.objects.get_or_create(customer = customer,complete= False)
    orderItem, created = OrderItem.objects.get_or_create(order = order,productvariant= productvariant)
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
    else:
        items = []
        cartItems=[]
        order = {'get_cart_items':0, 'get_cart_total':0}
    id = request.GET.get('id','')
    product = Product.objects.get(id=id)
    categories = Category.objects.filter(is_sub= False)
    active_category= request.GET.get('category','')
    productvariants = ProductVariant.objects.filter(product=product)
    colors = Color.objects.filter(productvariant__in=productvariants).distinct()
    sizes = Size.objects.all()

    context = {
        'product': product,
        'colors': colors,
        'sizes': sizes,
        'categories': categories,
        'active_category': active_category,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        }
    return render(request,'app/detail.html',context)


def addcart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        cartItems = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}

    id = request.GET.get('id', '')
    try:
        product = Product.objects.get(id=id)
        productvariants = ProductVariant.objects.filter(product=product)
        colors = Color.objects.filter(productvariant__in=productvariants).distinct()
        sizes = Size.objects.all()
        categories = Category.objects.filter(is_sub=False)
        active_category = request.GET.get('category', '')
        context = {
            'product': product,
            'colors': colors,
            'sizes': sizes,
            'categories': categories,
            'active_category': active_category,
            'items': items,
            'order': order,
            'cartItems': cartItems,
        }

        return render(request, 'app/addcart.html', context)

    except Product.DoesNotExist:
        return HttpResponse("Product not found.")


class ProductvariantAPI(APIView):
    def get(self, request):
        try:
            productvariants = ProductVariant.objects.all()
            # Sử dụng serializer để chuyển đổi dữ liệu thành định dạng phản hồi mong muốn
            mydata = GetAllProductvariant(productvariants, many=True)
            # Trả về phản hồi
            return Response(data=mydata.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(data={'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def contact_view(request):
     return redirect('https://mail.google.com/')


def alert(request):
    return render(request,  "app/alert.html")
