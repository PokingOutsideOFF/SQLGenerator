from django.urls import path
from .views import *
urlpatterns = [
    path('', Login,name="login"),    #login
    path('register/',Register,name="register"),  #register
    path("verify-otp/", VerifyOTP, name="verify-otp"),  #verify email 
    path("otp-verification/", VerifyOTPPage, name="verifyotppage"),#to show otp verification page
    path("forgot-password-email/", FpEmailPage, name="fpemailpage"),#to show reset email page
    path('forgot_password/',FpEmail,name="forgot_password"),#reset email verification
    path("fp-otp/", FpOTP, name="fp-otp"),                  #reset password otp
    path("fp-password/", FpPassword, name="fp-password"),   #reset password
    path('home/', home,name="home"),
    # path("logout/", Logout, name="logout"),

    path('upload_csv/', upload_csv, name='upload_csv'),
    path('chat_history/', ChatHistoryPage, name='chat_history'),

    # path('upload/excel/', upload_excel, name='upload_excel')

]

