from django.db import models
from ProductTypes.models import ProductTypes

# # Tables

class Brands(models.Model):

    brand_name = models.CharField(max_length=300,null=True,blank=True)
    
class ProductsModel(models.Model):

    product_name         = models.CharField(max_length=300,default="")
    product_image_tag    = models.CharField(max_length=300,null=True,blank=True)
    product_type         = models.ForeignKey(ProductTypes,on_delete=models.CASCADE)
    brands               = models.ForeignKey(Brands,on_delete=models.CASCADE)
    price                = models.FloatField(null=True,blank=True)
    retailer             = models.CharField(max_length=300,null=True,blank=True)

# Specific Product Type Tables

class CoffeTables(models.Model):
    
    product             = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    style               = models.CharField(max_length=300,null=True,blank=True)
    shape               = models.CharField(max_length=300,null=True,blank=True)
    material            = models.CharField(max_length=300,null=True,blank=True)
    size                = models.CharField(max_length=300,null=True,blank=True)
    finish              = models.CharField(max_length=300,null=True,blank=True)
    seating_capacity    = models.CharField(max_length=300,null=True,blank=True)
    features            = models.CharField(max_length=300,null=True,blank=True)
    frame_material      = models.CharField(max_length=300,null=True,blank=True)
    recommended_room    = models.CharField(max_length=300,null=True,blank=True)

class Laptops(models.Model):

    product              = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    screen_size          = models.CharField(max_length=300,null=True,blank=True)
    hard_drive_size      = models.CharField(max_length=300,null=True,blank=True)
    ram                  = models.CharField(max_length=300,null=True,blank=True)
    operating_system     = models.CharField(max_length=300,null=True,blank=True)
    processor_brand      = models.CharField(max_length=300,null=True,blank=True)
    processor_type       = models.CharField(max_length=300,null=True,blank=True)
    laptop_computer_type = models.CharField(max_length=300,null=True,blank=True)
    memory_capacity      = models.CharField(max_length=300,null=True,blank=True)
    wireless_capability  = models.CharField(max_length=300,null=True,blank=True)
    color                = models.CharField(max_length=300,null=True,blank=True)

class FreshFruit(models.Model):

    product             = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    fruit_type          = models.CharField(max_length=300,null=True,blank=True)
    form                = models.CharField(max_length=300,null=True,blank=True)
    special_diet_needs  = models.CharField(max_length=300,null=True,blank=True)

class Cookies(models.Model):

    product             = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    food_condition      = models.CharField(max_length=300,null=True,blank=True)
    flavor              = models.CharField(max_length=300,null=True,blank=True)
    cookie_type         = models.CharField(max_length=300,null=True,blank=True)
    special_diet_needs  = models.CharField(max_length=300,null=True,blank=True)

class EnergyDrinks(models.Model):

    product             = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    form                = models.CharField(max_length=300,null=True,blank=True)
    container           = models.CharField(max_length=300,null=True,blank=True)
    fruit_type          = models.CharField(max_length=300,null=True,blank=True)
    special_diet_needs  = models.CharField(max_length=300,null=True,blank=True)





    























