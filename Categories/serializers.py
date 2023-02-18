from rest_framework import serializers
from .models import Categories
from Departments.serializers import DepartmentsSerializer
from Departments.models import Departments
class CategoriesSerializer(serializers.ModelSerializer):

    department = DepartmentsSerializer(Departments,read_only=True)
    class Meta:
        model = Categories
        fields = (  'id',
                    'category_name',
                    'department'
                 )

