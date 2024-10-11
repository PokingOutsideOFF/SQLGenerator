from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import random

from .serializers import *
from .models import User

class GetUserView(APIView):
    def get(self,requests):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

def send_otp_email(otp, email):
    subject = "Verify your Email - {}".format(email)
    message = "Your 4-digit OTP for your account is : " + str(otp) + ". Please don't share it with anyone else"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email').lower()
        fnd1 = User.objects.filter(email=email)

        if fnd1.exists():  # User already exists
            messages.error(request, "Email already exists. Please login.")
            return Response({"error": "Email already exists. Please login"}, status=status.HTTP_400_BAD_REQUEST)  # Redirect to login page

        username = request.data.get('username')
        fnd2 = User.objects.filter(username=username)
        if fnd2.exists():
            messages.error(request, "Username already exists")
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)  # Redirect to login page


        password = request.data.get('password')
        confirmPassword = request.data.get('confirm_password')

        if password != confirmPassword:
            messages.error(request, "Password and Confirm Password do not match. Please try again.")
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST) # Redirect back to registration page
        
        otp = random.randint(1000, 9999)
        print(otp)

        send_otp_email(otp, email)
        messages.success(request, "OTP is sent to your email. Please enter it.")
        return Response({"succcess": "OTP sent to your email.", "otp": otp, "password": password}, status=status.HTTP_201_CREATED)

class CreateUser(APIView):
    def post(self, request):
        user = User.objects.create(
            username = request.data.get("username"),
            email = request.data.get("email"),
            password = request.data.get("password")
        )
        if user:
            return Response({"succcess": "User created. Please login."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User created. Please login."}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView((APIView)):
    def post(self, request):
        print("here")
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email)
        if user.exists():
            request.session['otp'] = random.randint(1000, 9999)
            print(f"Generated OTP: {request.session['otp']}")  # Debugging line
            send_otp_email(request.session['otp'], email)
            return Response({"succcess": "Email exists.", "otp": request.session['otp']}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"User does not exist.Please register"}, status=status.HTTP_400_BAD_REQUEST)


# class VerifyOTPView(APIView):
#     def post(self, request):
#         mainotp = request.data.get('otp')
#         print(request.session.items())
#         print(f"Received OTP: {mainotp}, Session OTP: 2")
#         if 2 == int(mainotp):
#             applicant = User.objects.create(
#                 username=Username,
#                 email=Email,
#                 password=Password
#             )
#             del request.session['password']
#             del request.session['email']
#             del request.session['username']

#             del request.session['otp']
#             Username = ""
#             Email = ""
#             Password = ""
#             Sessionotp = ""

#             messages.success(request, "You have Registered successfully. Login to continue.")

#             return Response({"succcess": "User created. Please login."}, status=status.HTTP_201_CREATED)
#         else:
#             messages.error(request, "Invalid OTP. Please try again")
#             return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        # if request.data.get('reset') == "false":
        #     username = request.data.get('username')
        #     email = request.data.get('email')
        #     print("For account creation")

        # mainotp = request.data.get('otp')

        # if int(request.data.get('ogotp')) == int(mainotp):
        #     if request.data.get('reset') == "false":
        #         applicant = User.objects.create(
        #             username=username,
        #             email=email,
        #             password=request.data.get('password')
        #         )
        #     else:
        #         return Response({"message": "Reset link activate"}, status=status.HTTP_201_CREATED)

        #     return Response({"message": "User created and verified successfully."}, status=status.HTTP_201_CREATED)

        # return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        print(user.password)
        if user:
            if check_password(password, user.password):
                return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:         
            return Response({"error": "User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
    

# class ForgotPasswordView(APIView):
#     def post(self, request):
#         serializer = ResetPasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             try:
#                 otp = random.randint(1000, 9999)
                
#                 send_otp_email(otp, email)
#                 return Response({"message": "OTP sent to email.","otp":otp}, status=status.HTTP_200_OK)
#             except User.DoesNotExist:
#                 return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        print(email)
        password = request.data.get('password')
        user =User.objects.filter(email = email).first()
        if user:
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # def post(self, request):
    #     serializer = SetNewPasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         email = request.data.get('email')
    #         user = User.objects.filter(email = email).first()
    #         if user:
    #             user.set_password(serializer.validated_data['password'])
    #             user.save()
    #             return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


