from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.status import (HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED)
# from django.db.models import Q
from utilities.product_type_classes import product_types
from django.db.models import Count,Max
from .models import Departments
from .serializers import DepartmentsSerializer


class DepartmentsEndpoint(APIView):
    """
    

    """
    def post(self,request):

        request_body = request.data
        
        new_department = Departments.objects.create(   

                                    department_name = str(request_body.get('department_name', None)) )
        
        response_data = {

            "message":"Department created",
            "department":DepartmentsSerializer(new_department).data
        }

        return Response(response_data, status=HTTP_200_OK)

class GetAllDepartmentsEndpoint(APIView):
    """
    

    """

    def get(self,request):

        request_body = request.data
        
        all_deparments = Departments.objects.all()   

        response_data = {

            "message":"Showing all departments",
            "departments":DepartmentsSerializer(all_deparments,many=True).data
        }

        return Response(response_data, status=HTTP_200_OK)