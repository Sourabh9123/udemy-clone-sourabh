from rest_framework import generics
from rest_framework.response import Response
from accounts_user.serializers import UserSerializer, LoginSerializer,PasswordChangeSerializer, PasswordResetSerializer, SetResetPasswordSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from accounts_user.models import User, ResetPasswordByEmail
from rest_framework.views import APIView

from django.db import transaction
import json
import random

from django.core.mail import send_mail
from django.shortcuts import render



from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




def generate_otp(length=6):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp    



class SignupView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def post(self,  request, *args, **kwargs):
        data = request.data

        serializer = UserSerializer(data=data)
      
        user = User.objects.filter(email=data.get('email'))
        if user:
            return Response('User already exists please login')
       
       
        if serializer.is_valid():
            password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = password
            serializer.save()
            return Response({"user":serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        
            
        
        
        
            
            
            
            

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def post(self,  request, *args, **kwargs):
        serializer  = LoginSerializer(data=request.data)
        is_user = User.objects.filter(email=request.data['email']).exists()
       
        try:
           
            if serializer .is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                
                user= authenticate(request, username=email, password=password)
                login(request, user)
                
                user_token = get_tokens_for_user(user)
                user_data = User.objects.get(email = email )
                user_serializer_data = UserSerializer(user_data)
                
                
                return  Response({"user":user_serializer_data.data, "token": user_token}, status=status.HTTP_200_OK)
        except Exception as e:

            if is_user:
                return Response({'message':'password does not match'},status=status.HTTP_400_BAD_REQUEST )
            return Response({'message':'user does not exist'},status=status.HTTP_400_BAD_REQUEST )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
                
            
            
class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        
        access = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        access_token = request.auth
        refresh_token =  request.data.get('refresh_token')
        print(f"access token---------------{access_token}, --------- ref tok {refresh_token} -------------- , access--- {access}")
        
        user = request.user
        email = user.email
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password =  serializer.validated_data.get('new_password')
            authenticate_user = authenticate(request, username = email, password = old_password )
            if authenticate_user:
                user.set_password(new_password)
                user.save()
                return Response({"password change successfully"}, status=status.HTTP_200_OK)
            return Response({"Not valid password"}, status=status.HTTP_200_OK)  
                
        return Response({"something went wrong"}, status=status.HTTP_200_OK)      
                    
                
                
            
            
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        logout(request)
        return Response('Successfully Logout')
    
    
    


    

class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request, *args , **kwargs):
        
        with transaction.atomic():
            data = request.data
            
            if 'email' in data:
                email = data.get('email')
                is_user = User.objects.filter(email= email).exists()
                if is_user:
                    
                    otp = generate_otp()
                    print("Generated OTP:", otp)
                    data['otp'] = otp
                    
                    seriliazer = PasswordResetSerializer(data=data)
                    if seriliazer.is_valid():
                        seriliazer.save()
                        ############################### send email function here
                        link_to_reset = "http://127.0.0.1:8000/api/account/set-password/"
                        subject = 'password reset link'
                        message = f"the otp is {otp} and the link is{link_to_reset}"
                        from_email = "udemy clone"
                        recipient_list = [email]

                        send_mail(subject, message, from_email, recipient_list)

                        
                        ###############################
                        return Response('a link has been sent to your register email address please chcek your email')
                
        return Response("sorry this is not a register email")
    
    
password_of_email= "rulgbbuyqweckcmf"



class SetResetPassword(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SetResetPasswordSerializer
    
    def post(self, request, *args ,**kwargs ):
        data = request.data
        with transaction.atomic():
            serializer = SetResetPasswordSerializer(data=data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                otp_verify = serializer.validated_data.get('otp')
                password = serializer.validated_data.get('password')
                confirm_password = serializer.validated_data.get('confirm_password')
                print(email, otp_verify, password, confirm_password)
                if password == confirm_password:
                    is_user = ResetPasswordByEmail.objects.filter(email=email).exists()
                    
                    no_user = User.objects.filter(email=email).exists()
                    if not no_user:
                        return Response("no user with this email please check yout email")
                    
                    if is_user:
                        user_to_set_passowrd = ResetPasswordByEmail.objects.filter(email=email).order_by('-created_at').first()
                        
                        otp = user_to_set_passowrd.otp 
                        if otp_verify == otp :
                            user = User.objects.get(email=email)
                            user.set_password(password)
                            user.save()
                            all_otp = ResetPasswordByEmail.objects.filter(email=email)
                            all_otp.delete()
                            return Response("password change successfully please login")
                    return Response("not valid otp please resend otp")
                return Response("password and confirm password doesn't match")
                
            
            return Response("please try again later") 





class TuitorSignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self,  request, *args, **kwargs):
        data = request.data
        data['role'] = "instructor"

        serializer = UserSerializer(data=data)
      
        user = User.objects.filter(email=data.get('email'))
        if user:
            return Response('User already exists please login')
       
        if serializer.is_valid():
            password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = password
            serializer.save()
         
            return Response({"user":serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            