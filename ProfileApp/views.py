from django.shortcuts import render

from AuthenticationApp import models


# Create your views here.
def getProfile(request):
    role = request.user.get_role()
    if role == 'student':
        userData = models.Student.objects.all()
        pageName = 'student'
    elif role == 'professor':

        pageName = 'professor'
    elif role == 'engineer':

        pageName = 'engineer'
    context = {
        'page_name' : pageName,
        'user_data' : userData,
    }
    return render(request, 'profile.html', context)
