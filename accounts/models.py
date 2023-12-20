from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
import os
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=64)
    useremail = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    #add
    age = models.IntegerField(default=0)
    sex = models.IntegerField(default=0)
    weight = models.CharField(max_length=200)
    diabetes = models.BooleanField(default=0)
    blood_pressure = models.BooleanField(default=0)
    
    
    def __str__(self):
        return self.username
    
    def publish(self):
        self.save()
    