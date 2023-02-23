from django.urls import path
from . import views

urlpatterns = [
    

    # By Product Name only

    path("products/product_name=<product_name>&filters=<filters>",views.Filter.as_view()),
    path("products/product_name=<product_name>",views.Filter.as_view()),
    
    path("products/",views.Filter.as_view()),

    # path("apply_filter/product_type=<str:product_type>&filters_applied=<filters_applied>",views.SelectedFilterEndpoint.as_view())
    
]