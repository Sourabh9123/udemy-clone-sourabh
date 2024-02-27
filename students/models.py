from django.db import models
import uuid
from django.contrib.auth import get_user_model
from accounts_user.models import User

User = get_user_model()


class Learner(models.Model):
    
    id = models.UUIDField(primary_key= True, default= uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='learner', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User , on_delete= models.CASCADE, related_name= "learner")
    
    

    def __str__(self):
        return self.name



