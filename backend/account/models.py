from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Time Stamp Mixin 
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

# class User(A)