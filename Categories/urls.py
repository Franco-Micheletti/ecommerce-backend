from django.urls import path
from . import views

urlpatterns = [

    path("categories/create",views.CategoriesEndpoint.as_view()),
    path("categories/all",views.GetAllCategoriesEndpoint.as_view())
]