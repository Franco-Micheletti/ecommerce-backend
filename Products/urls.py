from django.urls import path
from . import views

urlpatterns = [
    

    # Search With Filters
    path("products/product_name=<product_name>&filters=<filters>&page=<page>",views.SearchWithFilters.as_view()),
    # Search Without Filters
    path("products/product_name=<product_name>&page=<page>",views.SearchWithOutFilters.as_view()),
    # Products
    path("products/home",views.ProductsHome.as_view()),
    # Specific Product
    path("product/create",views.Product.as_view()),
    path("product/id=<id>",views.Product.as_view()),
    path("product/properties/id=<id>",views.GetProductProperties.as_view())

]