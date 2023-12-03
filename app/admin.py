from django.contrib import admin
from .models import *
# Register your models here.
# from .models import Variant

# class VariantInline(admin.TabularInline):
#     model = Variant

# class ProductAdmin(admin.ModelAdmin):
#     inlines = [VariantInline]

admin.site.register(Product)
# admin.site.register(Variant)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Category)