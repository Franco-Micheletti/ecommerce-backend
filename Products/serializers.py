from rest_framework import serializers
from .models import(ProductsModel,
                    Brand,
                    EnergyDrinks,Properties,Values,PropertyValuePairs,ProductProperties)

class BrandSerializer(serializers.ModelSerializer):

    class Meta:

        model = Brand
        fields = ('brand_name',)
        
class ProductsSerializer(serializers.ModelSerializer):
    
    brand    = BrandSerializer(Brand,read_only=True)
    
    class Meta:
        model = ProductsModel
        fields = (  'id',
                    'product_name',
                    'product_image_tag',
                    'product_type',
                    'brand',                                   
                    'price',
                    'retailer',
                    "quantity"
                  )
        
class PropertiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Properties
        fields = ('property_name',)

class ValuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Values
        fields = ('value_name',)

class PropertyValuePairsSerializer(serializers.ModelSerializer):
    
    property = PropertiesSerializer(read_only=True)
    value    = ValuesSerializer(read_only=True)
    
    class Meta:
        model = PropertyValuePairs
        fields = ('property',
                  'value')

class ProductPropertiesSerializer(serializers.ModelSerializer):

    property_value_pair = PropertyValuePairsSerializer(read_only=True)
    class Meta:
            model = ProductProperties
            fields = ('property_value_pair',)

class GetProductByPropertySerializer(serializers.ModelSerializer):

    product = ProductsSerializer(read_only=True)
    class Meta:
            model = ProductProperties
            fields = ('product',)

class EnergyDrinksSerializer(serializers.ModelSerializer):

    product = ProductsSerializer(ProductsModel,read_only=True)

    class Meta:
        model   = EnergyDrinks
        fields  = ( 'id',
                    'product',              
                    'flavor',
                    'special_diet_needs'                
                 )

