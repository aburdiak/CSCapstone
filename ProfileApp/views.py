from django.shortcuts import render

from AuthenticationApp import models


# Create your views here.
def getProfile(request):
    role = request.user.get_role()
    user_name = request.user.get_full_name()
    user_email = request.user.get_email()
    user_data = models.MyUser.objects.filter(email=user_email).values_list()
    user_data = user_data[0]
    user_active = user_data[6]
    user_admin = user_data[7]
    user_student = user_data[8]
    user_professor = user_data[9]
    user_engineer = user_data[10]
    if role == 'professor':
        professor_data = models.Professor.objects.filter(user=request.user).values_list()
        professor_data = professor_data[0]
        phone_number = professor_data[1]
        context = {
            'user_name': user_name,
            'user_data': user_data,
            'role': role,
            'role_data': phone_number,
            'role_var' : "Phone Number:",
        }
    elif role == 'student':
        student_data = models.Student.objects.filter(user=request.user).values_list()
        student_data = student_data[0]
        grad_year = student_data[1]
        context = {
            'user_name': user_name,
            'user_data': user_data,
            'role': role,
            'role_data': grad_year,
            'role_var' : "Graduation Year:",
        }
    elif role == 'engineer':
        engineer_data = models.Engineer.objects.filter(user=request.user).values_list()
        engineer_data = engineer_data[0]
        alma_mater = engineer_data[1]

        context = {
            'user_name': user_name,
            'user_data': user_data,
            'role': role,
            'role_data': alma_mater,
            'role_var' : "Alma Mater",
        }

    return render(request, 'profile.html', context)
