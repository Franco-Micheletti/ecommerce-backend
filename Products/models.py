from django.db import models
from ProductTypes.models import ProductTypes
import uuid
from login.models import CustomUser
# Tables

class Brand(models.Model):

    brand_name = models.CharField(max_length=300,null=True,blank=True)

class Properties(models.Model):
    property_name = models.CharField(max_length=300,null=True,blank=True)

class Values(models.Model):
    value_name = models.CharField(max_length=300,null=True,blank=True)

class PropertyValuePairs(models.Model):
    property = models.ForeignKey(Properties,on_delete=models.CASCADE)
    value    = models.ForeignKey(Values,on_delete=models.CASCADE)

class ProductsModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    product_name         = models.CharField(max_length=300,default="")
    product_image_tag    = models.CharField(max_length=300,null=True,blank=True)
    generic_image_tag    = models.CharField(max_length=300,null=True,blank=True)
    total_images         = models.IntegerField(null=True,blank=True)
    product_type         = models.ForeignKey(ProductTypes,on_delete=models.CASCADE)
    brand                = models.ForeignKey(Brand,on_delete=models.CASCADE)
    price                = models.FloatField(null=True,blank=True)
    retailer             = models.CharField(max_length=300,null=True,blank=True)
    quantity             = models.SmallIntegerField(default=1,null=True,blank=True)
    variant_id           = models.PositiveBigIntegerField(null=True,blank=True)
    variant_options      = models.JSONField(null=True,blank=True)
    date                 = models.DateField(auto_now_add=True,null=True,blank=True)
    pack                 = models.IntegerField(null=True,blank=True)
    availability         = models.BooleanField(null=True,blank=True)
    shipping_days        = models.IntegerField(null=True,blank=True)

class ProductVariants(models.Model):
    product     = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    variant_id  = models.PositiveBigIntegerField(null=True,blank=True)
    values      = models.JSONField(null=True,blank=True)

class ProductProperties(models.Model):
    product             = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    property_value_pair = models.ForeignKey(PropertyValuePairs,on_delete=models.CASCADE)

class FreshFruit(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )

    product             = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    fruit_type          = models.CharField(max_length=300,null=True,blank=True)
    form                = models.CharField(max_length=300,null=True,blank=True)
    special_diet_needs  = models.CharField(max_length=300,null=True,blank=True)

class Cookies(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )

    product             = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    food_condition      = models.CharField(max_length=300,null=True,blank=True)
    flavor              = models.CharField(max_length=300,null=True,blank=True)
    cookie_type         = models.CharField(max_length=300,null=True,blank=True)
    special_diet_needs  = models.CharField(max_length=300,null=True,blank=True)

class EnergyDrinks(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    
    product             = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    flavor              = models.CharField(max_length=300,null=True,blank=True)
    special_diet_needs  = models.CharField(max_length=300,null=True,blank=True)

class Favorites(models.Model):

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    
class UserReviews(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )

    product             = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    user                = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    text                = models.TextField(max_length=300,null=True,blank=True)
    score               = models.IntegerField(null=True,blank=True)
    date                = models.DateField(null=True,blank=True)
    





















