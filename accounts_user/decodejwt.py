from datetime import timedelta
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse


def decode_jwt(token):   # print(decode_jwt(request.auth)) this is the way we get access token
    token = str(token)
    try:
        decoded_token = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
        # it take signing key from simple jwt setting which you have done in settings.py and take ALGORITHM 
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    except jwt.DecodeError:
        return {"error": "Invalid token."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid JWT token."}
    
    

def get_refresh_token(request):
    try:
        
        refresh_token = RefreshToken.for_user(request.user)
        return JsonResponse({'refresh_token': str(refresh_token)})  # when you get the value access it by .content 
    except  Exception as e :
        return (f"something went wrong {str(e)}")




# print(request.auth)
# decode = decode_jwt(token=request.auth)
# print(decode)
# refresh = get_refresh_token(request)
# print(refresh.content)

# # print(request.META)
# # Retrieve IP address of the client
# client_ip = request.META.get('REMOTE_ADDR')

# # Retrieve user agent string
# user_agent = request.META.get('HTTP_USER_AGENT')

# # Print the values
# print("Client IP:", client_ip)
# print("User-Agent:", user_agent)