from django.urls import path
from . import views
from login.views import LoginView

urlpatterns = [
    path('login/',LoginView.as_view(),name = "login")
]
