from django.urls import path
from . import views

urlpatterns = [
    

    # Search With Filters
    path("products/product_name=<product_name>&filters=<filters>&page=<page>",views.SearchWithFilters.as_view()),
    # Search Without Filters
    path("products/product_name=<product_name>&page=<page>",views.SearchWithOutFilters.as_view()),
    # Products
    path("products/home",views.ProductsHome.as_view()),
    # Create Product
    path("product/create",views.Product.as_view()),
    # test
    path("test/",views.Test.as_view()),
    # Get Product
    path("product/id=<id>",views.Product.as_view()),
    # Get Product By Property
    path("product/property=<property>&value=<value>",views.GetProductsByProperty.as_view())
    
    
]