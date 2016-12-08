"""GroupsApp Models

Created by Naman Patwari on 10/10/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    members = models.ManyToManyField(MyUser)
    
    def __str__(self):
        return self.name

class GroupComment(models.Model):
    group_name = models.CharField(max_length=30, null=True)
    user = models.CharField(max_length=30, null=True)
    time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=500)

class AddUserByEmail(models.Model):
    user_email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
