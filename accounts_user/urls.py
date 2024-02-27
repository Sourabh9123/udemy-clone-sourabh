from django.urls import path
from accounts_user.views import (SignupView, LoginView, ChangePasswordView, 
                                 LogoutView, ResetPasswordView, SetResetPassword,
                                 TuitorSignUpView
                                 )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('signup/',SignupView.as_view(), name="signup_user" ),
    path('tuitor-signup/',TuitorSignUpView.as_view(), name="tuitor" ),
    path('login/',LoginView.as_view(), name="login_user" ),
    path('change-password/',ChangePasswordView.as_view(), name="change-password" ),
    path('logout/',LogoutView.as_view(), name="logout" ),
    path('password-reset/',ResetPasswordView.as_view(), name="password-reset" ), # only takes email and send otp and link
    path('set-password/',SetResetPassword.as_view(), name="set-passwordt" ), # takes otp that is sent by server and takes password , confirm passwoed and email
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    
]