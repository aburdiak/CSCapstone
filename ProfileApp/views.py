from django.shortcuts import render

from . import models

# Create your views here.
def getProfile(request):
    return render(request, 'profile.html')
