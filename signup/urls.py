from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup),
    path('activate/<token>/<id>/',views.activate_account)
]