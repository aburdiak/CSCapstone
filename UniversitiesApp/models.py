"""
UniversitiesApp Models

Created by Jacob Dunbar on 11/5/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="static/universityimages", default=0)
    description = models.CharField(max_length=300)
    website = models.CharField(max_length=300, default="/")
    members = models.ManyToManyField(MyUser)
    
    def __str__(self):
        return self.name
	
class Course(models.Model):
    tag = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    members = models.ManyToManyField(MyUser)
    professor = models.CharField(max_length=200, null=True)	

    def __str__(self):
	return self.name

class AddStudentByEmail(models.Model):
    student_email = models.EmailField(
        verbose_name='email address',
	max_length=200,	
	unique=True,
    )

