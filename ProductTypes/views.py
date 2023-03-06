from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import ProductTypes
from ProductTypes.models import ProductTypes
from .serializers import ProductTypesSerializer
from rest_framework.status import (HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED)
from django.db.models import Q
from utilities.product_type_classes import product_types
from django.db.models import Count,Max
import json
from Categories.models import Categories

class ProductType(APIView):

    def post(self,request):
        
        request_data = request.data

        new_product_type = ProductTypes.objects.create(

            product_type_name = request_data["product_type_name"],
            category = Categories.objects.get(id=request_data["category"])

        )

        new_product_type_data = ProductTypesSerializer(new_product_type).data

        return Response({"message":"Product Type created successfully",
                        "new_product_type":new_product_type_data},status=HTTP_200_OK)
    
class GetAllProductTypes(APIView):

    def get(self,request):

        all_product_types = ProductTypes.objects.all()

        all_product_types_data = ProductTypesSerializer(all_product_types,many=True).data
        
        response_data = {
                            "product_types":all_product_types_data
                        }
        return Response(response_data,status=HTTP_200_OK)