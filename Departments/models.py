from django.db import models

class Departments(models.Model):

    department_name = models.CharField(max_length=200,null=True,blank=True)
