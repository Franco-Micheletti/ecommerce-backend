from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.status import HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_400_BAD_REQUEST
from django.core.mail import send_mail
from django.conf import settings


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
    def post(request):
        """
        Creates a new user with the data provided:

        1- Takes a list of arguments:

        - first_name: Your First Name
        - last_name: Your Last Name
        - username: For Account Login
        - email: Valid Email
        - password: Hashed password for Account Login

        EXAMPLE JSON DATA

            {
                "first_name":"Franco",
                "last_name":"Micheletti",
                "username":"franco",
                "email":"franmich1720@gmail.com",
                "password":"1234"
            }

        """
        # Get request data

        data = request.data

        # Check if the username doesn't exist in the database
        try:
            check_username = User.objects.get(username = data["username"] )
            if check_username:
                return Response("THE USERNAME ALREADY EXISTS, PICK ANOTHER ONE",status=HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # Check if the email doesn't exist in the database
            try:
                check_email = User.objects.get(email = data["email"] )
                if check_email:
                    return Response("THIS EMAIL IS ALREADY REGISTERED!",status=HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                
                # Create user ( Abstract User Creation )
                user = User.objects.create(
                                        first_name = data["first_name"],
                                        last_name  = data["last_name"],
                                        username   = data["username"],
                                        email      = data["email"],
                                        password   = data["password"],
                                        is_active  = 0 
                )

                user.set_password(data["password"])
                user.save()
                token = Token.objects.create(user=user)
                token_key = token.key

                # Verification email

                name = data["first_name"]
                recipient_email = data["email"]

                verification_email(name, recipient_email, token_key, str(user.id))

                response_body = {
                    
                    "status": "successful",
                    "user_id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "email": user.email,
                    "message": "Successfully registered your account"
                }

                return Response(response_body,status=HTTP_200_OK)

