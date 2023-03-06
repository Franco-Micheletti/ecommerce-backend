from django.urls import path
from . import views

urlpatterns = [

    path("product_types/all",views.GetAllProductTypes.as_view()),
    
    path("product_type/create",views.ProductType.as_view())
]