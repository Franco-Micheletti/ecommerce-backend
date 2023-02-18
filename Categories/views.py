from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.status import (HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED)
# from django.db.models import Q
from django.db.models import Count,Max
from .models import Categories
from .serializers import CategoriesSerializer

class CategoriesEndpoint(APIView):
    """
    

    """
    def post(self,request):
        
        request_body = request.data
        
        new_category = Categories.objects.create(
                                    
                                    category_name = request_body["category_name"],
                                    department    = request_body["department"] 
        )

        response_data = {

            "message":"Department created",
            "department":CategoriesSerializer(new_category).data
        }

        return Response(response_data, status=HTTP_200_OK)

class GetAllCategoriesEndpoint(APIView):
    """
    

    """

    def get(self,request):

        request_body = request.data
        
        all_categories = Categories.objects.all()   

        response_data = {

            "message":"Showing all categories",
            "categories":CategoriesSerializer(all_categories,many=True).data
        }

        return Response(response_data, status=HTTP_200_OK)