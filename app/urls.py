from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart , name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('register/', views.registerUser.as_view(), name="register"),
    path('login/', views.loginUser.as_view(), name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('search/', views.search, name="search"),
    path('category/', views.category, name="category"),
    path('detail/', views.detail, name="detail"),
    path('contact/', views.contact_view, name="contact"),
    path('save_shipping_address/', views.save_shipping_address, name="save_shipping_address"),
    path('productvariant_api/',views.ProductvariantAPI.as_view(), name ="productvariant_api"),
     path('alert/', views.alert, name="alert"),
]
