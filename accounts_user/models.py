from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name,  is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            first_name = first_name,
            last_name = last_name,
         
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name,**extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name,**extra_fields):
        user = self._create_user(email, password,first_name, last_name, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    roles = (('learner','learner'),
             ('instructor','instructor'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # username = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verified_instructor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    email_verified =models.BooleanField(default=False) 
    role = models.CharField(choices=roles, default='learner',max_length=40 )
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', "last_name"]

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


    def __str__(self):
        return self.email
    
    
    
    


class ResetPasswordByEmail(models.Model):
    email = models.EmailField(null=True, blank=True)
    otp = models.CharField(max_length =10)
    created_at =models.DateTimeField(auto_now_add=True, null=True)
    
    
    
    def __str__(self):
        return self.email
    
    
    
    