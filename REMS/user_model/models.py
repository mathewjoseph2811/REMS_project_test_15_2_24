from django.db import models
from django.db import models
from django.db.models.fields import TextField, EmailField
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.
# class user_data(AbstractBaseUser):
#     first_name = TextField(blank= False, null= False)
#     last_name = TextField()
#     Email = EmailField(blank= False, null= False, unique=True)
#     USERNAME_FIELD = 'Email'