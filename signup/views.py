from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.authtoken.models import Token
from login.models import CustomUser
from rest_framework.status import HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST
from django.core.mail import send_mail
from django.conf import settings
import uuid
import datetime
import re
#---------------------------------- VERIFICATION EMAIL -----------------------------------------

def verification_email(name,recipient_email,token,id):
    """
    Sends an email to the new created user's email with a link to verify their account.
    """
    subject = "[Codename: Market] Please Verify Your Email Address"
    link = "Verification Link : http://127.0.0.1/activate/"+str(token)+"/"+id
    message = " Hi "+ str(name) + "welcome to Codename: Market, please access this link to verify your email " + str(link)
    html_content = "<div> </div>"
    
    send_mail(

        subject         = subject,
        from_email      = settings.EMAIL_HOST_USER,
        recipient_list  = [recipient_email],
        message         = message,
        html_message    = html_content,
        fail_silently   = False
    )

#------------------------------ SIGNUP ( REGISTRATION ) ----------------------------

class Signup(APIView):
    def post(self,request):
        """
        Creates a new user with the data provided:

        1- Takes a list of arguments:

        - first_name: Your First Name
        - last_name: Your Last Name
        - username: For Account Login
        - email: Valid Email
        - password: Hashed password for Account Login

        """
        # Get request data

        data = request.data

        # Check if the username doesn't exist in the database
        try:
            check_username = CustomUser.objects.get(username = data["username"] )
            if check_username:
                return Response({"message":"Username not available pick another one"},status=HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            # Check if the email doesn't exist in the database
            try:
                check_email = CustomUser.objects.get(email = data["email"] )
                if check_email:
                    return Response({"message":"This email belongs to another account"},status=HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                # Check if the date is a valid format
                try:
                    datetime.date.fromisoformat(data["birthday"])
                except:
                    return Response({"message":"Birthday is required for legal issues"},status=HTTP_400_BAD_REQUEST)
                # Check if the email is valid
                if len(data["email"]) < 3 or "@" not in data["email"]:
                    return Response({"message":"Email is required to activate your account after registration"},status=HTTP_400_BAD_REQUEST)
                # Check strong password
                password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
                is_valid = re.match(password_pattern, data["password"])
                if is_valid == None:
                    return Response({"message":"""A strong password should have:,
                                                  ,At least 8 characters in length.
                                                  ,At least one uppercase English letter.
                                                  ,At least one lowercase English letter.
                                                  ,At least one digit.
                                                  ,At least one special character."""},status=HTTP_400_BAD_REQUEST)
                # Create user ( Abstract User Creation )
                user = CustomUser.objects.create(
                first_name = data["firstname"],
                last_name  = data["lastname"],
                username   = data["username"],
                email      = data["email"],
                password   = data["password"],
                birthday   = data["birthday"],
                phone      = data["phone"],
                is_active  = 0 
                )

                user.set_password(data["password"])
                user.save()

                # Verification email

                name = data["firstname"]
                recipient_email = data["email"]

                # verification_email(name, recipient_email, token_key, str(user.id))

                response_body = {
            
                    "user_id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "email": user.email,
                    "message": "Register Successfully"
                }

                return Response(response_body,status=HTTP_200_OK)

