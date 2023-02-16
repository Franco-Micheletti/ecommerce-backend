from django.urls import path
from . import views

urlpatterns = [
    

    # By Product Name only

    path("products/product_name=<product_name>",views.Filter.as_view()),
    
    path("products/",views.Filter.as_view()),
    
    path("paly_info/",views.Paly.as_view())
]