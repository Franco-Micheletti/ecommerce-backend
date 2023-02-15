from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import ProductsModel,CoffeTables
from .serializers import ProductsSerializer,CoffeTablesSerializer
from rest_framework.status import (HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED)
# from django.db.models import Q
from utilities.product_type_classes import product_types
from django.db.models import Count,Max

class Filter(APIView):
    def get(self,request,product_name=None):

        response_data = {
                            "filters":{
                                "Price":{
                                    "max_price":0
                                }
                            }
                        }
        
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

                # Create list of product types
                for field in product_types[most_popular_product_type][0]._meta.get_fields()[3:]:
                    
                    product_type_fields_list.append(field.name)

                # Add each filter ( a column in DB table ) to the filters key in response_data
                for column in product_type_fields_list:
                    
                    column = column.capitalize().replace("_"," ")
                    response_data["filters"][column] = {} 

                # 0 - For model of the product type
                products = product_types[most_popular_product_type][0].objects.filter(product__product_name__icontains=str(product_name))
                
                # Count each possible value in attribute
                for column in product_type_fields_list:
                    values = products.values(column)
                    for value in values:
                        try:
                            response_data["filters"][column.capitalize().replace("_"," ")][value[column]] += 1
                        except:
                            response_data["filters"][column.capitalize().replace("_"," ")][value[column]] = 1

                # 1 - For serializer of the product type
                products_data = product_types[most_popular_product_type][1](products,many=True).data
                
                # Get maximum price of products
                max_price = CoffeTables.objects.aggregate(Max('product__price'))
                response_data["filters"]["Price"]["max_price"] = max_price['product__price__max']
                # Response
                response_data["products"] = products_data
                
                return Response(response_data,status=HTTP_200_OK)
            else:
                return Response({},status=HTTP_200_OK)
        else:
            
            all_products = ProductsModel.objects.all()
            response_data = {"products":ProductsSerializer(all_products,many=True).data}
            
            return Response(response_data,status=HTTP_200_OK)

            