from django.contrib import admin
from .models import Size
from .models import Category
from .models import Product
from .models import  ProductVariant
from .models import Order
from .models import OrderItem
from .models import ShippingAddress
from .models import Color
from django.utils.html import format_html

admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

# Register your models here.

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'size','price', 'product', 'display_image')
    search_fields = ('name',)
    readonly_fields = ['display_image']

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}"  height="55" />'.format(obj.image.url))
        else:
            return "No Image"
    display_image.short_description = 'Image'

admin.site.register(ProductVariant, ProductVariantAdmin)



class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'colored_color')
    search_fields = ('name',)
    def colored_color(self, obj):
        return format_html('<div style="width: 50px; height: 20px; background-color: {};"></div>', obj.color_id)
    colored_color.short_description = 'Color'

admin.site.register(Color, ColorAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=( 'name', 'price_avg', 'shoe_type','display_image')
    search_fields = ('name',)
    readonly_fields = ['display_image']

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}"  height="55" />'.format(obj.image.url))
        else:
            return "No Image"
    display_image.short_description = 'Image'

admin.site.register(Product, ProductAdmin)
