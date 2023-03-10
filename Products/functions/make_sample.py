from Products.models import ProductsModel
from rest_framework.response import Response
from rest_framework.status import (HTTP_400_BAD_REQUEST)

def make_sample(product_name):

    if len(str(product_name)) > 3:
        sample = ProductsModel.objects.filter(product_name__icontains=str(product_name))[:20]
        return sample
    else:
        return Response({"info":"min_characters",
                            "message":"Search text must have more than 3 letters"},status=HTTP_400_BAD_REQUEST)
    