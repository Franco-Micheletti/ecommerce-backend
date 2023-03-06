from rest_framework import serializers
from Categories.serializers import CategoriesSerializer
from .models import ProductTypes

class ProductTypesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    class Meta:
        model = ProductTypes
        fields = (  'id',
                    'product_type_name',
                    'category'
                 )

