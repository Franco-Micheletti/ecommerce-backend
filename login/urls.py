from django.urls import path
from . import views
from login.views import LoginView,Logout,CookieTokenRefreshView,GetUserData
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/',LoginView.as_view(),name = "login"),
    path('logout/',Logout.as_view(),name = "logout"),
    path('refresh_token/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('user/id=<id>',GetUserData.as_view(),name = "user"),
]
