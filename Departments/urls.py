from django.urls import path
from . import views

urlpatterns = [

    path("departments/all",views.GetAllDepartmentsEndpoint.as_view()),
    
    path("departments/create",views.DepartmentsEndpoint.as_view()),
    
]