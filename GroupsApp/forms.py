"""GroupsApp Forms

Created by Naman Patwari on 10/10/2016.
"""
from django import forms

class GroupForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=300)

class GroupCommentForm(forms.Form):
    comment = forms.CharField(label='Text', max_length=500)

class AddUserByEmailForm(forms.Form):
    user_email = forms.CharField(label='Email', max_length=255)
