from rest_framework import serializers
from .models import ProductVariant
class GetAllProductvariant(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields=("id","name", "size", "color","price","ImageURL", "product")