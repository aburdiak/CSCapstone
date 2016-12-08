"""
ProjectsApp Forms

Created by Lauren
"""


from django import forms
from django.forms import ModelForm
from .models import Project

class ProjectForm(ModelForm):
    '''
    name = forms.CharField(label='Project Name', max_length=200)
    description = forms.CharField(label='Description', max_length=10000)
    company = forms.CharField(label='Company Name', max_length=200)
    language = forms.CharField(label='Language', max_length=200)
    experience = forms.CharField(label='Experience', max_length=200)
    speciality = forms.CharField(label='Speciality', max_length=200)
    '''

    class Meta:
        model = Project
        fields = ('name','description','company','language','experience','speciality')


