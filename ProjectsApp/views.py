"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404

from .forms import ProjectForm
from django.utils import timezone
from django.shortcuts import redirect
from . import models
from . import forms

def getProjects(request):
	projects_list = models.Project.objects.all()
	return render(request, 'projects.html', {
        'projects': projects_list,
    })

def getProject(request):
	return render(request, 'project.html')

def createProject(request):
	if request.user.is_engineer:
		
		if request.method == 'POST':
			form = forms.ProjectForm(request.POST)
			if form.is_valid():
				print "form valid"	
				
				new_project = models.Project(name=form.cleaned_data['name'],description=form.cleaned_data['description'],company=form.cleaned_data['company'],language=form.cleaned_data['language'],experience=form.cleaned_data['experience'],speciality=form.cleaned_data['speciality'])	
						 
				new_project.save()

				namevar=form.cleaned_data['name']

				context = {
					"form": form,
					"head_title": "Create Project",
					"page_name": "Create Project",
					"button_value": "Submit",
					"name": namevar,
				}
				
				
				return render(request, 'project_created.html', context)
		else:
			print "err"
			form = forms.ProjectForm()
			context = {
				"form": form,
				"head_title": "Create Project",
				"page_name": "Create Project",
				"button_value": "Submit",
			} 
			return render(request, 'create_project.html', context)
	else:

		print "invalid user"
		return render(request, 'autherror.html')
