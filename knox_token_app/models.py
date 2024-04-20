from django.db import models
from django.contrib.auth.models import PermissionsMixin,BaseUserManager,AbstractUser
from django.utils import timezone
# Create your models here.

#MAIN USER MODEL
class UserManager(BaseUserManager):

    def _create_user(self,username,email,password,role,is_staff,is_superuser,**extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        now=timezone.now()
        email = self.normalize_email(email).lower()
        user=self.model(
            username=username.lower(),
            email=email,
            role=role,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,username,email,password,role,**extra_fields):
        return self._create_user(username,email,password,role,True,False,**extra_fields)
    
    def create_superuser(self,username,email,password,role,**extra_fields):
        user=self._create_user(username,email,password,role,True,True,**extra_fields)
        return user
    
class User(AbstractUser,PermissionsMixin):
    email = models.EmailField(unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # ROLES
    GENERALUSER = 1
    CONTRIBUTER = 2
    RESEARCHER = 3
    FIELDWORKER = 4
    REVIEWER = 5
    ADMIN = 6

    ROLE_CHOICES = (
        (GENERALUSER,'General User'),
        (CONTRIBUTER, 'Continous Contributer'),
        (RESEARCHER, "Researcher"),
        (FIELDWORKER, 'Field Workers'),
        (REVIEWER, 'Reviewer'),
        (ADMIN, 'Admin'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ["username","role"]

    def __str__(self):
        return self.email