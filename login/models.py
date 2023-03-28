from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):

    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4,unique=True, editable=False)
    birthday            = models.DateField(null=True,blank=True)
    phone               = models.CharField(max_length=300,null=True,blank=True)
    profile_image_tag   = models.CharField(max_length=300,null=True,blank=True)