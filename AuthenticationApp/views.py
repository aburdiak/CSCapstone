"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


from .forms import LoginForm, RegisterForm, UpdateForm
from .models import MyUser, Student, Teacher, Engineer

# Auth Views

def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if next_url is None:
		next_url = "/"
	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			messages.success(request, 'Success! Welcome, '+(user.first_name or ""))
			login(request, user)
			return HttpResponseRedirect(next_url)
		else:
			messages.warning(request, 'Invalid username or password.')
			
	context = {
		"form": form,
		"page_name" : "Login",
		"button_value" : "Login",
		"links" : ["register"],
	}
	return render(request, 'auth_form.html', context)

def auth_logout(request):
	logout(request)
	messages.success(request, 'Success, you are now logged out')
	return render(request, 'index.html')

def auth_register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        role = form.cleaned_data['role']
        student = False
        teacher = False
        engineer = False
        if role == 'student':
            student = True
        elif role == 'teacher':
            teacher = True
        elif role ==  'engineer':
            engineer = True

        new_user = MyUser.objects.create_user(email=form.cleaned_data['email'],
            password=form.cleaned_data["password2"],
            first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'],
            is_student=student, is_teacher=teacher, is_engineer=engineer)

        print form.cleaned_data['firstname']
        print new_user.first_name
        new_user.save()
        #Also registering students
        if role == 'student':
            new_student = Student(user = new_user)
            new_student.save()
        elif role == 'teacher':
            new_teacher = Teacher(user = new_user)
            new_teacher.save()
        elif role == 'engineer':
            new_enginer = Engineer(user = new_user)
            new_enginer.save()
        login(request, new_user);
        if role == 'student':
            messages.success(request, 'Success! Your student account was created.')
        elif role == 'teacher':
            messages.success(request, 'Success! Your teacher account was created.')
        elif role == 'engineer':
            messages.success(request, 'Success! Your engineer account was created.')
        messages.success(request, 'Success! Your account was created.')
        return render(request, 'index.html')

    context = {
        "form": form,
        "page_name" : "Register",
        "button_value" : "Register",
        "links" : ["login"],
    }
    return render(request, 'auth_form.html', context)

@login_required
def update_profile(request):
	form = UpdateForm(request.POST or None, instance=request.user)
	if form.is_valid():
		form.save()
		messages.success(request, 'Success, your profile was saved!')

	context = {
		"form": form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'auth_form.html', context)
