"""ProjectsApp Models

Created by Harris Christiansen on 10/02/16.
"""
from django.db import models
from django.utils import timezone
from AuthenticationApp.models import MyUser


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO Task 3.5: Add field for company relationship

    company = models.CharField(max_length=200)

    # TODO Task 3.5: Add fields for project qualifications (minimum required: programming language, years of experience, speciality)

    language = models.CharField(max_length=200)
    experience = models.CharField(max_length=200)
    speciality = models.CharField(max_length=200)
    #group_members = models.ManyToManyField(MyUser, null=True)

    def __str__(self):
        return self.name
