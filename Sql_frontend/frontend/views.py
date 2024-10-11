
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.exceptions import ValidationError
from .forms import UploadFileForm
# import openpyxl
import csv
import requests

API_BASE_URL = "http://127.0.0.1:8000/api/auth/" 

def home(request):
        return render(request, 'frontend/home.html')


def send_otp_email(otp, email):
    subject = "Verify your Email - {}".format(email)
    print(otp)
    message = "Your 4-digit OTP to verify your account is : " + str(otp) + ". Please don't share it with anyone else"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def send_psw_email(otp, email):
    subject = "Reset your Password - {}".format(email)
    print(otp)
    message = "Your 4-digit OTP to reset your password is : " + str(otp) + ". Please don't share it with anyone else"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        # Interact with register API
        response = requests.post(API_BASE_URL + 'register/', data={
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        })
        if response.status_code == 201:
            request.session['username'] = username
            request.session['email'] = email
            request.session['password'] = response.json().get('password')
            request.session['otp'] = response.json().get('otp')
            messages.success(request, "OTP is sent to your email. Please enter it.")
            return render(request, 'frontend/otp.html')  # Redirect to login page after successful registration
           
        else:
            error_message = response.json().get('error', 'Registration failed')
            messages.error(request, error_message)
            return render(request, 'frontend/register.html', {'error':error_message})

    return render(request, 'frontend/register.html')


def VerifyOTP(request):
    if request.method == "POST":
        print(request.session.get('username'))
        mainotp = request.POST['otp']

        if int(mainotp) == int(request.session.get('otp')): 
            response = requests.post(API_BASE_URL + 'create-user/', data={
                'username': request.session.get('username'),
                'email': request.session.get('email'),
                'password': request.session.get('password'),    
                'otp': mainotp
            })
            if response.status_code == 201:
                messages.success(request, "User created succesfully. Log in now")
               
                return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Enter again")
            return render(request, 'frontend/otp.html')

    else:
        print("Old request" + request)
        return render(request, "frontend/otp.html")
    
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Interact with login API
        response = requests.post(API_BASE_URL + 'login/', data={'username': username, 'password': password})
        if response.status_code == 200:
            request.session['username'] = username
            # messages.success(request, "User created succesfully. Log in now")
            return render(request,'frontend/home.html')  # Redirect to some home page after successful login
        else:
            errorData = response.json().get('error')
            # messages.error(request, errorData)
            return render(request, 'frontend/index.html', {'error': errorData})
    else:
        print("Printing view")
        return render(request, 'frontend/index.html')
    
def FpEmail(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        print(f"Received email: {email}")  # Debugging line
        response = requests.post(API_BASE_URL + 'verify-email/', data = {'email':email})

        if response.status_code == 201:
            request.session['email'] = email
            request.session['otp'] = response.json().get("otp")
            messages.success(request, "OTP is sent to your email. Please enter it.")
            return render(request, "frontend/reset_password_otp.html")
        
        else:   
            error_message = response.json().get('error')
            messages.error(request, error_message)
            return render(request, 'frontend/register.html', {'error':error_message})
    else:
        return render(request, "frontend/forgot_password.html")


# def Logout(request):
#     if 'email' in request.session:

#         del request.session['id']
#         del request.session['username']
#         del request.session['email']

#         return redirect("login")
#     else:
#         return redirect("login")


def VerifyOTPPage(request):
    return render(request, "frontend/otp.html")


def FpEmailPage(request):
    return render(request, "frontend/forgot_password.html")


def FpOTP(request):
    if request.method == "POST":
        email = request.session.get('email').lower()

        mainotp = request.POST['otp']
        if int(request.session.get('otp')) == int(mainotp):
            request.session['email'] = email
            del request.session['otp']
            messages.success(request, "Reset password link activated")
            return render(request, "frontend/reset_password.html")
        else:
            messages.error(request, "Invalid OTP. Please try again")
            return render(request, "frontend/reset_password_otp.html")


def FpPassword(request):
    if request.method == "POST":
        email = request.session.get("email")
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        print(email)
        if password == confirm_password:
            response = requests.post(API_BASE_URL + 'reset-password/', data = {'email':email, 'password':password})

            if response.status_code == 205:
                del request.session["email"]
                messages.success(request, "Password resetted successfully")
                return redirect("login")
            else:
                error_message = response.json().get('error', 'Registration failed')
                return render(request, 'frontend/reset_password.html', {'error':error_message})

        else: 
            return render(request, 'frontend/reset_password.html', {'error':"Passwords do not match"})



# def handle_uploaded_csv(f):
#     # Check file size (limit to 5MB)
#     if f.size > 5 * 1024 * 1024:
#         raise ValidationError("File size should be under 5MB")
#     print(f"Uploading file: {f.name}")
#     # Check file format
#     if not f.name.endswith('.csv'):
#         raise ValidationError("Unsupported file format. Please upload a CSV file.")

#     # Handle CSV file
#     try:
#         reader = csv.reader(f.read().decode('utf-8').splitlines())
#         for row in reader:
#             # Process each row
#             # print(row)
#             print(f"Processing row: {row}")
#             print("CSV file processed successfully")
#     except Exception as e:
#         print(f"Error processing CSV file: {e}")
#         raise ValidationError("Corrupted CSV file")

# def handle_uploaded_excel(f):
#     # Check file size (limit to 5MB)
#     print(f"Uploading file: {f.name}")
#     if f.size > 5 * 1024 * 1024:
#         raise ValidationError("File size should be under 5MB")
#     print("File size is within the limit")
#     # Check file format
#     if not (f.name.endswith('.xlsx') or f.name.endswith('.xls')):
#         raise ValidationError("Unsupported file format. Please upload an Excel file.")
#     print("File format is Excel")
#     # Handle Excel file
#     try:
#         wb = openpyxl.load_workbook(f)
#         sheet = wb.active
#         for row in sheet.iter_rows(values_only=True):
#             # Process each row
#             # print(row)
#             print(f"Processing row: {row}")
#             print("Excel file processed successfully")
#     except Exception as e:
#         print(f"Error processing Excel file: {e}")
#         raise ValidationError("Corrupted Excel file")


def upload_csv(request):
    csv_content = []
    if request.method == 'POST':
        csv_file = request.FILES.get('csvfile')

        decode_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decode_file)

        for row in reader:
            csv_content.append(', '.join(row))
        
        return render(request, 'frontend/home.html', {'csv_content':'\n'.join(csv_content)})
        # print("Received POST request for CSV upload")
        # form = UploadFileForm(request.POST, request.FILES)
        # print(form)
        # if form.is_valid():
        #     try:
        #         # handle_uploaded_csv(request.FILES['csvfile'])
        #         print("CSV file uploaded successfully")
        #         messages.success(request, 'CSV file uploaded successfully!')
        #     except ValidationError as e:
        #         form.add_error('csvfile', e)
        #         print(f"Validation error: {e}")
        #         messages.error(request, str(e))
        # else:
        #     print("Form is not valid")
        #     messages.error(request, 'Invalid form submission.')
        #     return render(request, 'frontend/home.html', {'form': form})
    # else:
    #     form = UploadFileForm()
    #     print("Rendering upload form for CSV")

    return render(request, 'frontend/home.html')


def upload_excel(request):
    if request.method == 'POST':
        print("Received POST request for Excel upload")
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         print("Form is valid")
    #         try:
    #             handle_uploaded_excel(request.FILES['excelfile'])
    #             print("Excel file uploaded successfully")
    #             messages.success(request, 'Excel file uploaded successfully!')
    #         except ValidationError as e:
    #             form.add_error('excelfile', e)
    #             print(f"Validation error: {e}")
    #             messages.error(request, str(e))
    #     else:
    #         print("Form is not valid")
    #         messages.error(request, 'Invalid form submission.')
    # else:
    #     form = UploadFileForm()
    #     print("Rendering upload form for Excel")

    return render(request, 'frontend/home.html')

def ChatHistoryPage(request):
    return render(request, "frontend/chat_history.html")