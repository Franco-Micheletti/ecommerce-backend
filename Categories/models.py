from django.db import models
from Departments.models import Departments

# Electronics Department

class Categories(models.Model):

    category_name = models.CharField(max_length=200,null=True,blank=True)
    department    = models.ForeignKey(Departments,on_delete=models.CASCADE)

