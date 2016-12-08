"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


from .forms import LoginForm, RegisterForm, UpdateFormStudent, UpdateFormEngineer, UpdateFormProfessor
from .models import MyUser, Student, Professor, Engineer

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

        ## Something about the following block of code causes issues setting the user name
        ## Current issue is unable to set user name and role status in database and other places

        role = form.cleaned_data['role']
        student = False
        professor = False
        engineer = False
        if role == 'student':
            student = True
        elif role == 'professor':
            professor = True
        elif role == 'engineer':
            engineer = True
        else:
            print "No role selected"

	    print "pre instantiation " + form.cleaned_data['firstname']
	    print "pre instantiation " + form.cleaned_data['role']
        n_uni = True
        if role == 'engineer':
            n_uni = False
        new_user = MyUser.objects.create_user(email=form.cleaned_data['email'],
                                              password=form.cleaned_data["password2"],
                                              first_name=form.cleaned_data['firstname'], last_name=form.cleaned_data['lastname'],
                                              is_student=student, is_professor=professor, is_engineer=engineer, needs_university=n_uni)


        print "post instatiation " + form.cleaned_data['firstname']
        #print "post instantiation " + new_user.first_name

        new_user.save()
        #Also registering students
        if role == 'student':
            new_student = Student(user = new_user)
            new_student.save()
        elif role == 'professor':
            new_professor = Professor(user = new_user)
            new_professor.save()
        elif role == 'engineer':
            new_enginer = Engineer(user = new_user)
            new_enginer.save()
        print new_user.get_full_name()
        #print new_student.get_full_name()
        login(request, new_user);
        if role == 'student':
            messages.success(request, 'Please choose your university.')
        elif role == 'professor':
            messages.success(request, 'Please choose your university.')
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
    print "In update profile"
    role = MyUser.get_role(request.user)
    if role == 'student':
        form = UpdateFormStudent(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success, your profile was saved!')
            student = Student(user = request.user)
            student.grad_year = form.cleaned_data['grad_year']
            student.save()
    elif role == 'professor':
        form = UpdateFormProfessor(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success, your profile was saved!')
            professor = Professor(user = request.user)
            professor.phone_number = form.cleaned_data['phone_number']
            professor.save()

    elif role == 'engineer':
        form = UpdateFormEngineer(request.POST or None, instance=request.user)
        print "Set Engineer form"
        if form.is_valid():
            form.save()
            messages.success(request, 'Success, your profile was saved!')
            print "form valid"
            engineer = Engineer(user = request.user)
            engineer.alma_mater = form.cleaned_data['alma_mater']
            engineer.save()

    print "After Conditionals"

    context = {
        "form": form,
        "page_name" : "Update",
        "button_value" : "Update",
        "role" : role,
        "links" : ["logout"],
    }
    return render(request, 'update_form.html', context)
