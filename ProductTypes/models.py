from django.db import models
from Categories.models import Categories


class ProductTypes(models.Model):
    
    product_type_name  = models.CharField(max_length=300,null=True,blank=True)
    category           = models.ForeignKey(Categories,on_delete=models.CASCADE)
   



