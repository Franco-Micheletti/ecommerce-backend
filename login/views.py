from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.status import HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.contrib.auth import authenticate

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }

class LoginView(APIView):
    
    def post(self, request, format=None):

        data = request.data
        response = Response()        
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)

                # access

                response.set_cookie(
                                    key = settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'], 
                                    value = data["access"],
                                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                    )
                
                # refresh 
                
                response.set_cookie(
                                    key = settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], 
                                    value = data["refresh"],
                                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                    )
                csrf.get_token(request)
                
                response.data = {"Success" : "Login successfully , cookies created , showing access token for testing purpouse.",
                                 "refresh":data['refresh'],
                                 "access":data['access']}
                
                return response
            else:
                return Response({"No active" : "This account is not active!!"},status=HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"},status=HTTP_404_NOT_FOUND)

