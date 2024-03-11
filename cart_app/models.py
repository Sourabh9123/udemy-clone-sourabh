from django.db import models
from django.contrib.auth import  get_user_model
from accounts_user.models import User
from students.models import Learner
import  uuid
from Instructor.models import Course

User = get_user_model()





  
class CartItem(models.Model):
    id  =  models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    
    
    def __str__(self):
        return self.course.title


class Cart(models.Model):
    id  =  models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    learner = models.OneToOneField(Learner,on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField('CartItem', related_name='cart_item')
    
    
    
    def __str__(self):
        return self.learner.name
    
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    order_id = models.CharField(max_length=100)
    signature = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    courses_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    
    



