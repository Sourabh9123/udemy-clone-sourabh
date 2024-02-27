from rest_framework.serializers import ModelSerializer
from accounts_user.models import  User, ResetPasswordByEmail
from rest_framework import serializers



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
        
        
        
class LoginSerializer(serializers.Serializer):
    email =serializers.EmailField()
    password = serializers.CharField(max_length=254, write_only=True)
    
    

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    


    
    
    
    
class PasswordResetSerializer(ModelSerializer):
    class Meta:
        model = ResetPasswordByEmail
        fields = "__all__"
        
        
    
    
    
class SetResetPasswordSerializer(serializers.Serializer):
    email  =  serializers.EmailField()
    otp = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=40)
    confirm_password = serializers.CharField(max_length=40)