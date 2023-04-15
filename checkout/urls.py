from django.urls import path
from . import views

urlpatterns = [

    # Mercado Pago Check out
    path("checkout/mercadopago",views.CheckoutMercadoPago.as_view()),
    
]