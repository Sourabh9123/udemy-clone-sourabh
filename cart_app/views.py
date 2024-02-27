from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from cart_app.serializers import CartSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from students.models import Learner
from Instructor.models import Course
from cart_app.models import Cart, CartItem
from rest_framework import  status
from rest_framework.response import  Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from Instructor.serializers import CourseSerializer
from django.http import JsonResponse
from razorpay import Client
import razorpay
from django.conf import settings






PUBLIC_KEY = "rzp_test_DqyEDw9vF6Y4kA",

SECRET_KEY ="uibpbafCZAypJUX226PdWxBs"





def initiate_payment(request):
    client = razorpay.Client(auth=("YOUR_API_KEY", "YOUR_API_SECRET"))
    payment = client.order.create({'amount': 50000, 'currency': 'INR', 'payment_capture': '1'})
    return JsonResponse(payment)






class AddToCartView(GenericAPIView):
    
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        
        is_learner  = request.user
        print(is_learner.role)
        if is_learner.role != "learner" :
            return Response("You are not a learner Please Create A learner account first",status=status.HTTP_401_UNAUTHORIZED)
        
        
            
        
        with transaction.atomic():
         
            user = request.user
            course_id = kwargs.get('course_id')
            
            course = get_object_or_404(Course, id=course_id)
            
        
            cartitem = CartItem.objects.filter(course=course).first()
            if not cartitem:
                cartitem = CartItem.objects.create(course=course)
                    
            
            is_learner = Learner.objects.filter(user=user)

            learner = get_object_or_404(Learner, user= user)
          
   
            cart , created = Cart.objects.get_or_create(learner=learner,)
            cart.items.add(cartitem)
            
            
            return Response("added to your cart", status=status.HTTP_200_OK)
            
            
            
        return Response("something went wrong", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        course_id = kwargs.get('course_id')
        
        course = get_object_or_404(Course, id=course_id)
        
        try:
            
            cartitem = CartItem.objects.filter(course=course)
            if not cartitem:
                cartitem = CartItem.objects.create(course=course)
                
        except Exception as e:
            pass
        
        cartitem.delete()
        
        return Response("successfully deleted", status=status.HTTP_204_NO_CONTENT)
        
            
    
    
    

class MyCartView(GenericAPIView):
    
    permission_classes = [IsAuthenticated]
    
    serializer_class = CartItemSerializer 
    
    def get(self, request, *args, **kwargs):
        
        
        user =  request.user
        learner = get_object_or_404(Learner, user=user)
        
        cart = get_object_or_404(Cart, learner=learner)
        
        cart_items = cart.items.all()
        
        courses_data = []
        for cart_item in cart_items:
            courses_data.append(cart_item.course)
            
        course_serializer = CourseSerializer(courses_data, many=True)

        serializer = CartSerializer(cart)
        data = course_serializer.data
        # data_without_leactures = [{k: v for k, v in item.items() if k != 'leactures'} for item in data]
        data_without_leactures = [{ k :v for k,v in item.items() if k != 'leactures'  }for item in data]
        
        if data_without_leactures:
            return Response(data_without_leactures, status=status.HTTP_200_OK)
        
        return Response("no courses add yet", status=status.HTTP_200_OK)
    
    
    
    
    
    
    
    
class PurchaseCourseView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        
        
        with transaction.atomic():
        
            data = request.data
            user =  request.user
            learner = Learner.objects.get(user=user)
            if learner:
                cart = Cart.objects.get(learner=learner)
                print("cart------------------------")
                if cart:
                    cartitems = cart.items.all()
                    to_be_pay = 0
                    for i in cartitems:
                        to_be_pay += i.course.price
                        
                                        
                    PUBLIC_KEY = "rzp_test_DqyEDw9vF6Y4kA",

                    SECRET_KEY ="uibpbafCZAypJUX226PdWxBs"

                    
                    
                    client = Client(auth=("rzp_test_DqyEDw9vF6Y4kA", "uibpbafCZAypJUX226PdWxBs"))
                    order_amount = int(to_be_pay * 100)  # Razorpay requires the amount in paisa
                    order_currency = 'INR'
                    order_receipt =  str(cart.id)
                    order = client.order.create({'amount': order_amount, 'currency': order_currency, 'receipt': order_receipt})
                    
                    # You may want to save the order ID in your database for reference
                    cart.order_id = order['id']
                    cart.save()
                    print("yes------------------------------------------------")
                    # Return the order details to the client
                    return Response({'order_id': order['id'], 'amount': order_amount}, status=status.HTTP_200_OK)

                    
                    
                    
                # here will come payment logic
                    
                    return Response("this is a error", status=status.HTTP_400_BAD_REQUEST)
                        
                    
                    
            else:
                return  Response("you are not a learner", status=status.HTTP_401_UNAUTHORIZED)     
                
            
        return Response("Something went Wrong", status=status.HTTP_400_BAD_REQUEST)
    
    
        

        
    
    
    
    