from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import ProductsModel,CoffeTables,Brand
from ProductTypes.models import ProductTypes
from .serializers import ProductsSerializer,CoffeTablesSerializer
from rest_framework.status import (HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED)
from django.db.models import Q
from utilities.product_type_classes import product_types
from django.db.models import Count,Max
import json

class Filter(APIView):
    """
    

    """
    def get(self,request,filters=None,product_name=None,page=1):

        response_data = {
                            "filters":{
                                "product_type":"",
                                "price":{
                                    "max_price":0
                                }
                            }
                        }
        
        # Price init 
        min_price = 0.01
        max_price = 0.01

        if product_name:
            if len(str(product_name)) > 3:
                sample = ProductsModel.objects.filter(product_name__icontains=str(product_name))[:20]
            else:
                return Response({"info":"min_characters",
                                 "message":"Search text must have more than 3 letters"},status=HTTP_400_BAD_REQUEST)

            if sample:

                # Count number of each product type for better searching
                # Then query the corresponding product type table

                product_type_ids = {}
                product_type_fields_list = []

                for product in sample:
                    try:
                        product_type_ids[product.product_type_id] += 1
                    except:
                        product_type_ids[product.product_type_id] = 1
                
                # Get the most popular product type dictionary
                most_popular_product_type = max(product_type_ids,key=product_type_ids.get)
                
                # Add the product_type to the JSON data

                response_data["filters"]["product_type"] = most_popular_product_type

                # Create list of product types
                for field in product_types[most_popular_product_type][0]._meta.get_fields()[3:]:
                    
                    product_type_fields_list.append(field.name)

                # Add each property ( a column in DB table ) to the filters key in response_data
                for column in product_type_fields_list:
                    
                    column = column
                    response_data["filters"][column] = {} 

                # 0 - For model of the product type
                product_type_model = product_types[most_popular_product_type][0]

                products = product_type_model.objects.filter(product__product_name__icontains=str(product_name))
                
                # Limit the results when filters are not applied , 
                # prevents the following error: "Cannot filter a query once a slice has been taken"

                if not filters:
                    products[0:1000]
                
                # Count each possible value in attribute
                for column in product_type_fields_list:
                    values = products.values(column)
                    for value in values:
                        try:
                            response_data["filters"][column][value[column]] += 1
                        except:
                            response_data["filters"][column][value[column]] = 1

                # Apply filters selected by the user before serializer
                
                if filters:
                    print(filters)
                    # Convert string to python dictionary
                    filters_json = json.loads(filters)
                    # Variable init
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
                    filtered_products = filtered_products[0:(int(page)*30)]
                    
                else:
                    # Without Filters selected by user
                    filtered_products = products[0:(int(page)*30)]
                
                
                # 1 - For serializer of the product type
                product_type_serializer = product_types[most_popular_product_type][1]
                # Serializing products by product type
                products_data = product_type_serializer(filtered_products,many=True).data
                
                # Get the maximum price of all products
                max_price = filtered_products.aggregate(Max('product__price'))
                response_data["filters"]["price"]["max_price"] = max_price['product__price__max']
                # add products to response data
                response_data["products"] = products_data
                # Add list of pages to render pages button in frontend
                if filters:
                    response_data["pages"] = [ x for x in range(1,round((len(total_products))/30)+1)]
                else:
                    response_data["pages"] = [ x for x in range(1,round((len(products))/30)+1)]
                
                return Response(response_data,status=HTTP_200_OK)
            else:
                return Response({},status=HTTP_200_OK)
        else:

            return Response(response_data,status=HTTP_200_OK)

class Product(APIView):

    def post(self,request):

        request_data = request.data
        
        # Create product

        new_product = ProductsModel.objects.create(
            
            product_name         = request_data["product_name"],
            product_image_tag    = request_data["product_image_tag"],
            product_type         = ProductTypes.objects.get(id=request_data["product_type_id"]),
            brand               = Brand.objects.get(id=request_data["brand_id"]),
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

        product_data = ProductsSerializer(product).data

        response_data = {
                            "product":product_data
                        }

        if product:
            return Response(response_data,status=HTTP_200_OK)
        
class ProductsHome(APIView):

    def get(self,request):

        products_home = ProductsModel.objects.all()[:12]
        products_home_data = ProductsSerializer(products_home,many=True).data
        
        if products_home:
            return Response(products_home_data,status=HTTP_200_OK)
        else:
            return Response({},HTTP_200_OK)
    
class GetProductProperties(APIView):

    def get(self,request,id):

        request_data = request.data

        product = ProductsModel.objects.get(id=id)
        
        if product:

            product_type_model            = product_types[product.product_type.id][0]
            product_type_model_serializer = product_types[product.product_type.id][1]

            product_type_object      = product_type_model.objects.get(product_id=id)
            product_type_object_data = product_type_model_serializer(product_type_object).data
            
            product_type_object_data.pop('id')
            product_type_object_data.pop('product')
            response_data = {
                                "product_properties":product_type_object_data
                            }
            
            return Response(response_data,status=HTTP_200_OK)
        else:
            return Response("No product have been found with the ID provided")