from django.db import models
import uuid
from accounts_user.models import User
from django.contrib.auth import get_user_model
from students.models import Learner

User = get_user_model() 

class Category(models.Model):
    title = models.CharField(max_length =200)
    
    
    def __str__(self) -> str:
        return self.title




class Instructor(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name ="instructor")
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='instructor', null=True, blank=True)
    specialities = models.TextField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name 
    

class Course(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(Instructor, on_delete = models.CASCADE, related_name= "instructor_courses")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    description = models.TextField(null=True, blank=True)
    learner = models.ManyToManyField(Learner, related_name='enrolled_courses', blank=True)
    tags = models.CharField(max_length = 300, null=True, blank=True)
    
    

    def __str__(self) -> str:
        return f"{self.title}"  
    
    
    
    
class Leacture(models.Model):
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(unique=True, blank=True, null=True)
    
    content = models.FileField(upload_to=None, max_length=100, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='leactures')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
        
    
    
    def save(self, *args, **kwargs):
        if not self.order:
            # Set the order field to the next available integer
            last_instance = Leacture.objects.order_by('-order').first()
            self.order = 1 if not last_instance else last_instance.order + 1

        super(Leacture, self).save(*args, **kwargs)
    
    


class RatingCourse(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name = "rating")
    rating = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "courses_rated")
    
    class Meta:
        # unique_together = ("id", 'user.id')
        unique_together = ('course', 'user')
        
    

    def __str__(self):
        return f"{self.user.first_name} 'rated' {self.course.title} 'this course :'- {self.rating}"
    
    
    