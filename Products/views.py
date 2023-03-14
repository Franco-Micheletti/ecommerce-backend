from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import ProductsModel,Properties,Values,PropertyValuePairs,Variants,ProductProperties,Brand
from ProductTypes.models import ProductTypes
from .serializers import (ProductsSerializer,PropertiesSerializer,ValuesSerializer,PropertyValuePairsSerializer,
ProductPropertiesSerializer,GetProductByPropertySerializer)
from rest_framework.status import (HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED)
from django.db.models import Q
from utilities.product_type_classes import product_types
from django.db.models import Count,Max
import json
import math
from Products.functions.make_sample import make_sample
from Products.functions.get_product_type_data import get_product_type_data
from Products.functions.count_different_values_of_each_column import count_different_values_of_each_column
import re

class SearchWithFilters(APIView):
    """
    METHODS:

    GET

    Returns products and filters filtering by product name and user applied filters
    """
    def get(self,request,filters,product_name,page=1):

        if product_name and filters and page:
            sample = make_sample(product_name)
            if sample:
                # Creates response data with the product properties.
                # Each type of product have different properties , we need to find the product type first.
                # The function returns the matching product type based on the sample result
                
                (response_data,matching_product_type,product_type_fields_list) = get_product_type_data(sample)
                
                # Now that we know the model we can make a bigger and more precise search 
                # looking for a name that matches the query in the matching product type's table

                product_type_model = product_types[matching_product_type][0]
                product_type_serializer = product_types[matching_product_type][1]
                products = product_type_model.objects.filter(product__product_name__icontains=str(product_name))
                
                # Count all the different values of each column
                
                response_data = count_different_values_of_each_column(response_data,products,product_type_fields_list)

                # Apply filters selected by the user before serializing

                filters_json = json.loads(filters)
                filtered_products = products
                # FEATURES FILTER 
                if "features" in filters_json:
                    filtered_products = filtered_products.filter(**filters_json["features"]).distinct()
                # PRICE FILTER
                if "price" in filters_json:
                    min_price = filters_json["price"]["min_price"]
                    max_price = filters_json["price"]["max_price"]
                    filtered_products = filtered_products.filter(product__price__range=(min_price,max_price) ).distinct()
                # ADD OFFSET FOR PAGINATION
                total_products    = filtered_products[0:1000]
                filtered_products = filtered_products[(int(page)-1)*30:int(page)*30]
                    
                # Serializing products by product type
                products_data = product_type_serializer(filtered_products,many=True).data
                
                # Get the maximum price of all products
                max_price = filtered_products.aggregate(Max('product__price'))
                response_data["filters"]["price"]["max_price"] = max_price['product__price__max']
                # add products to response data
                response_data["products"] = products_data
                # Add list of pages to render pages button in frontend
                response_data["pages"] = [ x for x in range(1,math.ceil((len(total_products))/30)+1)]
                response_data["total_results"] = len(total_products)
                
                return Response(response_data,status=HTTP_200_OK)
            else:
                return Response({"match":0},status=HTTP_200_OK)
        else:
            response_data = {"message":"Missing parameters"}
            return Response(response_data,status=HTTP_400_BAD_REQUEST)

class SearchWithOutFilters(APIView):
    """
    METHODS:
    
    GET

    Returns products and filters filtering by product name
    """
    def get(self,request,product_name,page):

        if product_name:
                
                response_data = {
                    "filters":{
                        "price":{
                            "max_price":0
                        }
                    }
                }

                products = ProductsModel.objects.filter(product_name__icontains=str(product_name))[0:1000]
                product_properties = ProductProperties.objects.filter(product__product_name__icontains=str(product_name))[0:1000]
                if product_properties:
                    for object in product_properties:
                        try:
                            response_data["filters"][object.property_value_pair.property.property_name] += 1
                        except:
                            response_data["filters"][object.property_value_pair.property.property_name] = 1

                if product_properties:
                    
                    # Results per page

                    products_slice = products[(int(page)-1)*30:int(page)*30]
                    
                    # Serializing objects

                    products_data = ProductsSerializer(products_slice,many=True).data

                    # Add products to response data

                    response_data["products"] = products_data

                    # Get the maximum price of all products

                    max_price = products.aggregate(Max('price'))
                    response_data["filters"]["price"]["max_price"] = max_price['price__max']

                    # Add list of pages to render pages button in frontend

                    response_data["pages"] = [ x for x in range(1,math.ceil((len(products))/30)+1)]
                    response_data["total_results"] = len(products)
                    
                    return Response(response_data,status=HTTP_200_OK)
                else:
                    return Response({"match":0},status=HTTP_200_OK) 
        else:
            response_data = {"message":"Product name not provided"}
            return Response(response_data,status=HTTP_400_BAD_REQUEST)
        
class Product(APIView):

    def post(self,request):

        request_data = request.data
        
        # Create product

        new_product = ProductsModel.objects.create(
            
            product_name         = request_data["product_name"],
            product_image_tag    = request_data["product_image_tag"],
            product_type         = ProductTypes.objects.get(id=request_data["product_type_id"]),
            brand                = Brand.objects.get(id=request_data["brand_id"]),
            price                = request_data["price"],
            retailer             = request_data["retailer"]
        )

        product_type_model            = product_types[request_data["product_type_id"]][0]
        product_type_model_serializer = product_types[request_data["product_type_id"]][1]
        
        # Create dictionary of variables and values used to create category objects dynamically
        try:
            fields_and_values = {field.name:request_data.get("properties","")[field.name] for field in product_type_model._meta.get_fields()[2:]}
            fields_and_values["product"] = new_product
        except KeyError as error:
            print("\033[1;31;40m"+"ERROR - Key "+"\033]"+"\033[1;36;40m"+"'"+error.args[0]+"'"+"\033]"+"\033[1;31;40m"+" not found \033]\n")
            
        
        # Create product properties object
        new_product_type_object = product_type_model.objects.create(**fields_and_values)
        
        # Create serializers
        new_product_type_object_data = product_type_model_serializer(new_product_type_object).data
        new_product_data = ProductsSerializer(new_product).data

        return Response({"message":"Product created successfully",
                        "product":{"basic_data":new_product_data,
                                   "properties":new_product_type_object_data}},status=HTTP_200_OK)
    
    def get(self,request,id):

        product = ProductsModel.objects.get(id=id)

        if product:
            
            product_type_model            = product_types[product.product_type.id][0]
            product_type_model_serializer = product_types[product.product_type.id][1]

            product_type_object      = product_type_model.objects.get(product_id=id)
            product_type_object_data = product_type_model_serializer(product_type_object).data
            
            product_type_object_data.pop('id')

            response_data = {"basic":product_type_object_data["product"]}

            product_type_object_data.pop('product')

            response_data["properties"] = product_type_object_data
           
            return Response(response_data,status=HTTP_200_OK)
        else:
            return Response("No product have been found with the ID provided")

    def delete(self,request,id):

        product = ProductsModel.objects.get(id=id)

        if product:
            product.delete()

            return Response("Product deleted successfully",HTTP_200_OK)
        else:
            return Response("Product doesn't exist",HTTP_400_BAD_REQUEST)
    
    def put(self,request,id):

        return Response({},HTTP_200_OK)
    
class ProductsHome(APIView):

    def get(self,request):

        products_home = ProductsModel.objects.all()[:12]
        products_home_data = ProductsSerializer(products_home,many=True).data
        
        if products_home:
            return Response(products_home_data,status=HTTP_200_OK)
        else:
            return Response({},HTTP_200_OK)
    
        
class Test(APIView):

    def post(self,request):

        request_data = request.data

        new_product = ProductsModel.objects.create(
            
            product_name         = request_data["product_name"],
            product_image_tag    = request_data["product_image_tag"],
            product_type         = ProductTypes.objects.get(id=request_data["product_type_id"]),
            brand                = Brand.objects.get(id=request_data["brand_id"]),
            price                = request_data["price"],
            retailer             = request_data["retailer"]
        )

        properties = request_data["properties"]

        if properties:
            for dict_ in properties:
                
                property = Properties.objects.get_or_create(property_name=dict_[0])
                value    = Values.objects.get_or_create(value_name=dict_[1])
                property_value_pair = PropertyValuePairs.objects.get_or_create(property=property[0],value=value[0])
                product_properties  = ProductProperties.objects.get_or_create(product=new_product,property_value_pair=property_value_pair[0])
            
            # If successful

            # product_properties_queryset = ProductProperties.objects.filter(product=new_product)
            # properties_data = {object.property_value_pair.property.property_name:object.property_value_pair.value.value_name for object in product_properties_queryset }
            
            response_data = {
                "message":"product created successfully",
                "product":new_product.id
            }

            return Response(response_data,status=HTTP_200_OK)
        else:
            return Response("Properties is required",HTTP_400_BAD_REQUEST)

class GetProductsByProperty(APIView):

    def get(self,request,property,value):

        response_data = {}
        
        try:
            property_object = Properties.objects.get(property_name=property)
            value_object    = Values.objects.get(value_name=value)
            property_value_pair = PropertyValuePairs.objects.get(property=property_object,value=value_object)
        except:
            return Response("Property/Value pair not found",status=HTTP_400_BAD_REQUEST)
        product_properties_objects = ProductProperties.objects.filter(property_value_pair=property_value_pair)
        
        if product_properties_objects:
            
            for index,object in enumerate(product_properties_objects):
                product_properties_queryset = ProductProperties.objects.filter(product=object.product)
                properties_data = {object.property_value_pair.property.property_name:object.property_value_pair.value.value_name for object in product_properties_queryset }
                response_data[index] = ProductsSerializer(object.product).data
                response_data[index]["properties"] = properties_data        
            
            return Response(response_data,status=HTTP_200_OK)                                  
        
        else:
            return Response("Property pair not found",status=HTTP_400_BAD_REQUEST)
        
        