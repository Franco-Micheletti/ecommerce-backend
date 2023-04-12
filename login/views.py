from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.status import HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import serializers as jwt_serializers,exceptions as jwt_exceptions,views as jwt_views,tokens
from django.middleware import csrf
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser
import rest_framework.exceptions as exceptions
from rest_framework import exceptions, serializers
from .serializers import UserSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }

class LoginView(APIView):

    @permission_classes((IsAuthenticated))
    def post(self, request, format=None):

        data = request.data
        response = Response()        
        username = data.get('username', None)
        password = data.get('password', None)
        try:
            user = CustomUser.objects.get(username=username)
            password = user.check_password(password)
        except:
            return Response({"message" : "Invalid username or password"},status=HTTP_400_BAD_REQUEST)
        if user and password:
            
            data = get_tokens_for_user(user)
                
            # access
            
            response.set_cookie(
                                key = settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'], 
                                value = data["access"],
                                expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                max_age  = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                )
            
            # refresh 
            
            response.set_cookie(
                                key = settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], 
                                value = data["refresh"],
                                expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                                max_age  = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                )
            csrf.get_token(request)
            
            response.data = {"message":"Login Successfully",
                                "refresh":data['refresh'],
                                "access":data['access'],
                                "expires_in":settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']}
            return response
            # else:
            #     return Response({"message" : "This account is not active, check your email and activate your account"},status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({"message" : "Invalid username or password"},status=HTTP_400_BAD_REQUEST)

class Logout(APIView):
    
    @permission_classes((IsAuthenticated))
    def post(self,request):
        try:
            refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
            token = RefreshToken(refresh_token)
            token.blacklist()

            response = Response()
            
            # THIS CODE WILL REMOVE COOKIE CREATED WHILE USING POSTMAN , HOWEVER THIS IS NOT WORKING IN THE BROWSER

            response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_ACCESS"] ,path='/',domain='127.0.0.1' )
            response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"] ,path='/',domain='127.0.0.1')
            response.delete_cookie("csrftoken")

            # REMOVES ACCESS COOKIE BY SETTING EXPIRES TO 0 AND MAX_AGE TO 0

            response.set_cookie(
                                key = settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'], 
                                path='/',
                                expires = 0,
                                max_age=0,
                                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                )
                
            # REMOVES REFRESH COOKIE BY SETTING EXPIRES TO 0 AND MAX_AGE TO 0

            response.set_cookie(key = settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], 
                                path='/',
                                expires = 0,
                                max_age=0,
                                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                )

            response.data = {"message":"Logout successfully"}
            return response
        except Exception as err:
            
            raise exceptions.ParseError(err)

class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken
    
    def validate(self, attrs):

        refresh = self.token_class(attrs["refresh"])
        data = {"access": str(refresh.access_token)}

        try:
            # Attempt to blacklist the given refresh token
            access_token = refresh.access_token
            access_token.blacklist()
        except AttributeError:
            pass

        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()

        data["refresh"] = str(refresh)

        return data

class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    
    def post(self,request):

        response = Response()
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
        
        if refresh_token != None:
            refresh    = RefreshToken(refresh_token,verify=True)
            
            serializer = CookieTokenRefreshSerializer(data={"refresh":str(refresh)})
            try:
                serializer.is_valid(raise_exception=True)
            except jwt_exceptions.TokenError as e:
                raise jwt_exceptions.InvalidToken(e.args[0])
            
            response.set_cookie(
                                key      = settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'], 
                                value    = serializer.validated_data['access'],
                                expires  = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                max_age  = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                secure   = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                )

            response.data = {"jwt_access":str(serializer.validated_data['access'])}

            # Add this to the response data if you want to update the refresh token along with access token
            # "jwt_refresh":str(serializer.validated_data['refresh']) 

            return response
        else:
            return Response("Invalid token",status=HTTP_400_BAD_REQUEST)

class GetUserData(APIView):

    def get(self,request,id):

        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response("Invalid Token",HTTP_401_UNAUTHORIZED)
        
        user_data = UserSerializer(user).data
        
        return Response(user_data,status=HTTP_200_OK)
        
        