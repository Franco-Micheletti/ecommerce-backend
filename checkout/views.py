import mercadopago as mp
from rest_framework.views import APIView,Response
import os
from rest_framework.status import (HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR)

class CheckoutMercadoPago(APIView):

    def post(self,request):
        
        request_data = request.data
        if "items" in request_data:
            items_list = request_data["items"]
        
            sdk = mp.SDK(os.getenv('MERCADO_PAGO_PRIVATE_KEY'))

            preference_data = {
                "items": items_list
            }

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]
        else:
            return Response("Missing items to create preference",HTTP_400_BAD_REQUEST)
        return Response(preference,status=HTTP_200_OK)


