from django.urls import path
from . import views
from login.views import LoginView

urlpatterns = [
    path('user_login/',LoginView.as_view(),name = "user_login")
]
