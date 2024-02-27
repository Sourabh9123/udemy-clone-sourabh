# In your app's signals.py file
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts_user.models import User
from django.contrib.auth import get_user_model
from Instructor.models import Instructor
from students.models import Learner
User = get_user_model()

@receiver(post_save, sender=User)
def new_user_created(sender, instance, created, **kwargs):
    
    if created:
        try:
            name = instance.first_name + " " + instance.last_name
    
            if instance.role == 'instructor':
                
                instructor = Instructor.objects.create(name = name, user=instance, )
                instructor.save()
                print(f"a new instructor joined {instance.first_name}")
            
            
            
                
            # Logic to perform when a new user is created (e.g., send a welcome email)
                # print(f"a new instructor joined {instance.first_name}")
        except Exception as e:
            print(e)
            