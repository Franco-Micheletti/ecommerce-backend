from django.urls import path
from . import views

urlpatterns = [
    

    # By Product Name only
    path("products/product_name=<product_name>&filters=<filters>&page=<page>",views.Filter.as_view()),
    
    path("products/product_name=<product_name>&page=<page>",views.Filter.as_view()),
    
    
    path("products/home",views.ProductsHome.as_view()),
    path("product/create",views.Product.as_view()),
    path("product/id=<id>",views.Product.as_view()),
    path("product/properties/id=<id>",views.GetProductProperties.as_view())

]