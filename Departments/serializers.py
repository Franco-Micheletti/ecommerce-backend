from rest_framework import serializers
from .models import Departments
          
class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = (  'id',
                    'department_name'
                 )

