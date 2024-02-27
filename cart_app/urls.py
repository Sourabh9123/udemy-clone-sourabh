from django.urls import  path
from cart_app.views import AddToCartView, MyCartView, PurchaseCourseView

urlpatterns = [
    path('<uuid:course_id>/',AddToCartView.as_view(), name='add-to-cart'),
    path('',MyCartView.as_view(), name="my-cart"),
    path('buy/', PurchaseCourseView.as_view(), name="buy-course")
    
    
]
