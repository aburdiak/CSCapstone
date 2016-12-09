"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from AuthenticationApp.models import Student
from AuthenticationApp.models import Professor
from AuthenticationApp.models import MyUser
from .models import University
from .models import Course
from django.contrib import messages

#list of universities
#links to university/all$
def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

#gets a single university
#link : /university?name=[universityname]
def getUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = University.objects.get(name__exact=in_name)
        is_member = in_university.members.filter(email__exact=request.user.email)
        is_professor = request.user.is_professor
	context = {
            'university' : in_university,
            'userIsMember': is_member,
	    'userIsProfessor': is_professor,
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')


#checks if user is authenticated, and gets a form to create a university
#links to /university/form$
def getUniversityForm(request):
    if request.user.is_authenticated():
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

#deals with creating the university object
#links to /formsuccess$ and then /university?name=[universityname]
def getUniversityFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
                new_university = University(name=form.cleaned_data['name'], 
                                             photo=request.FILES['photo'],  
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'universityformsuccess.html', context)
            else:
                return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

#join university
#links to /university/join?name=[universityname]
def joinUniversity(request):
    if request.user.is_authenticated():
        request.user.needs_university = False
        request.user.needs_company = False

        in_name = request.GET.get('name', 'None')
        in_university = University.objects.get(name__exact=in_name)
        in_university.members.add(request.user)
        in_university.save()
        request.user.university_set.add(in_university)
        request.user.save()

	is_professor = request.user.is_professor

        if request.user.is_student == True:
            stu = Student(user=request.user)
            stu.university = str(in_university)
            stu.save()
        elif request.user.is_professor == True:
            prof = Professor(user=request.user)
            prof.university = str(in_university)
            prof.save()
        context = {
            'university' : in_university,
            'userIsMember': True,
	    'userIsProfessor' : is_professor
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')

#unjoin university
#links to /university/unjoin?name=[universityname]     
def unjoinUniversity(request):
    if request.user.is_authenticated():
        request.user.needs_university = True
        request.user.needs_company = False
        in_name = request.GET.get('name', 'None')
        in_university = University.objects.get(name__exact=in_name)
        in_university.members.remove(request.user)
        in_university.save();
        request.user.university_set.remove(in_university)
        request.user.save()
        if request.user.is_student == True:
            stu = Student(user=request.user)
            stu.university = "no university"
            stu.save()
        elif request.user.is_professor == True:
            prof = Professor(user=request.user)
            prof.university = "no university"
            prof.save()
        context = {
            'university' : in_university,
            'userIsMember': False,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')

#fetches course
#links to /university/course$    
def getCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        is_member = in_course.members.filter(email__exact=request.user.email)
        

	is_professor = request.user.is_professor
	context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse' : is_member,
	    'userIsProfessor' : is_professor,
        }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

#links to a course form
#links to /university/course/
#this is broken
def courseForm(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = University.objects.get(name__exact=in_university_name)
        #course_name = request.POST["tag"]
	context = {
            'university': in_university,
	    #'course_name': course_name,
        }
        return render(request, 'courseform.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

#creates a course object and adds it
#links to /university/course/addcourse?name=[coursename]
#this is broken
def addCourse(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.CourseForm(request.POST)
            if form.is_valid():
                in_university_name = request.GET.get('name', 'None')
                in_university = University.objects.get(name__exact=in_university_name)
                if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
                    return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
                new_course = models.Course(tag=form.cleaned_data['tag'],
                                           name=form.cleaned_data['name'],
                                           description=form.cleaned_data['description'],
                                           university=in_university,professor=request.user.last_name)
                new_course.save()
                in_university.course_set.add(new_course)
                is_member = in_university.members.filter(email__exact=request.user.email)
                is_professor = request.user.is_professor

		context = {
		    'form': form,
                    'university' : in_university,
                    'userIsMember': is_member,
		    'userIsProfessor' : is_professor,
                    'course' : new_course,
		}
                return render(request, 'course_created.html', context)
            else:
                return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
        else:
            form = forms.CourseForm()
            return render(request, 'courseform.html')
        # render error page if user is not logged in
    return render(request, 'autherror.html')


#removes a course
#links to the original university page 
def removeCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = University.objects.get(name__exact=in_university_name)
        
	in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.delete()
        
	is_professor = request.user.is_professor
	is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember' : is_member,
	    'userIsProfessor' : is_professor,
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.members.add(request.user)
        in_course.save();
        request.user.course_set.add(in_course)
        request.user.save()

	is_professor= request.user.is_professor
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': True,
	    'userIsProfessor': is_professor,
        }
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def unjoinCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.members.remove(request.user)
        in_course.save();
        request.user.course_set.remove(in_course)
        request.user.save()
        
	is_professor = request.user.is_professor
	context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': False,
            'userIsProfessor': is_professor,
	}
        return render(request, 'course.html', context)
    return render(request, 'autherror.html')

def coursepage(request):
    if request.user.is_authenticated():
	university_name = request.GET.get('name', 'None')
	
        university_obj= University.objects.get(name__exact=university_name)

        course_tag = request.GET.get('course', 'None')
	in_course = university_obj.course_set.get(tag__exact=course_tag)
	
	is_professor = request.user.is_professor

	context = {
            'university.name' : university_name,    
            'course' : in_course,
            'course.members.all' : in_course.members.all,
            'university.photo' : university_obj.photo,
            'userIsProfessor' : is_professor,
        }

        return render(request, 'course.html', context)
    
    else:
        return render(request, 'autherror.html')



def addStudent(request):
    if request.user.is_authenticated():
    	if request.user.is_professor:
    	    print "professor adding student by email"
	    if request.method == 'POST':
    	           
         	#university_name = request.GET.get('name','None')
		prof_id = request.user.id

		professor_obj = Professor.objects.get(user_id__exact=prof_id)

		university_name = professor_obj.university		

		in_course_name = request.GET.get('course','None')

		student_email = request.POST["student_email"] 

		print university_name
		print in_course_name
		print student_email

		student_obj = MyUser.objects.get(email__exact=student_email)

		if student_obj.is_student:
			university_obj = University.objects.get(name__exact=university_name)


			#fix this#
			#in_course = university_obj.course_set.get(tag__exact=in_course_name)
        		in_course = Course.objects.get(tag__exact=in_course_name)
			in_course.members.add(student_obj)
        		in_course.save();		
			
	
			context = {
				'course.members.all' : in_course.members.all,
				'university.name' : university_name,
				'course.name' : in_course_name,
				'university.photo' : university_obj.photo,
				'course': in_course,
				'university_name': university_name,
			}
 			return render(request, 'added_success.html', context)
		else:
		    messages.warning(request, 'Student can not be added')
	    else:
		messages.warning(request, 'Student does not exist')

	else:
	    return render(request, 'course.html', context)    
    else:
    	return render(request, 'autherror.html');
    

