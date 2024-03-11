from rest_framework.serializers import ModelSerializer
from cart_app.models import Cart, CartItem, Payment
from rest_framework import  serializers
from Instructor.serializers import  CourseSerializer


        
        

    
        
        
        
class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__" 
        
        
        
        
class CartSerializer(ModelSerializer):
    # items = serializers.SerializerMethodField(read_only=True)
    items = CartItemSerializer(read_only=True, many=True)
    # new_data = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id','learner','items']
        
    
    # def get_new_data(self, obj):
    #     print(obj)
    #     cart = Cart.objects.
        

                
        
class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
            
            
        