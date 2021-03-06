"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from AuthenticationApp.models import MyUser

def getGroups(request):
    if request.user.is_authenticated():
        groups_list = models.Group.objects.all()
        context = {
            'groups' : groups_list,
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        comments_list = models.GroupComment.objects.filter(group_name=in_name)
        context = {
            'group' : in_group,
            'userIsMember': is_member,
            'comments': comments_list,
            'is_student' : request.user.is_student
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
                new_group.save()
                context = {
                    'name' : form.cleaned_data['name'],
                    'is_student': request.user.is_student
                }
                return render(request, 'groupformsuccess.html', context)
        else:
            form = forms.GroupForm()
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.add(request.user)
        in_group.save()
        request.user.group_set.add(in_group)
        request.user.save()
        comments_list = models.GroupComment.objects.filter(group_name=in_name)
        context = {
            'group' : in_group,
            'userIsMember': True,
            'comments': comments_list,
            'is_student': request.user.is_student
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    
def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.remove(request.user)
        in_group.save()
        request.user.group_set.remove(in_group)
        request.user.save()
        context = {
            'group' : in_group,
            'userIsMember': False,
            'is_student': request.user.is_student
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')


def addUserByEmail(request):

    if request.method == 'POST':
        form = forms.AddUserByEmailForm(request.POST)
        if form.is_valid():
            in_name = request.GET.get('name', 'None')
            in_email = form.cleaned_data['user_email']
            in_group = models.Group.objects.get(name__exact=in_name)
            is_member = in_group.members.filter(email__exact=request.user.email)
            comments_list = models.GroupComment.objects.filter(group_name__exact=in_name)
            context = {
                'group': in_group,
                'userIsMember': is_member,
                'comments': comments_list,
                'is_student': request.user.is_student
            }
            user_exists = models.MyUser.objects.filter(email__exact=in_email).exists()
            if user_exists:
                in_user = MyUser.objects.get(email__exact=in_email)
            else:
                return render(request, 'group.html', context)
            in_group.members.add(in_user)
            in_group.save();
            in_user.group_set.add(in_group)
            in_user.save()
            return render(request, 'group.html', context)
        else:
            return render(request, 'group.html')
    else:
        form = forms.AddUserByEmailForm()
        in_name = request.GET.get('name', 'None')
        comments_list = models.GroupComment.objects.filter(group_name__exact=in_name)
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        context = {
            'comments': comments_list,
            'form': form,
            'group': in_group,
            'userIsMember': is_member,
            'is_student': request.user.is_student
        }

    return render(request, 'group.html')



#Comment stuff
def getComments(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        comments_list = models.GroupComment.objects.filter(group_name=in_name)
        context = {
            'group' : in_group,
            'userIsMember': is_member,
            'comments': comments_list,
            'is_student': request.user.is_student
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupCommentForm(request):
    return render(request, 'group.html')

def addComment(request):
    if request.method == 'POST':
        form = forms.GroupCommentForm(request.POST)
        if form.is_valid():
            in_name = request.GET.get('name', 'None')
            new_comment = models.GroupComment(comment=form.cleaned_data['comment'], user=request.user, group_name=in_name)
            new_comment.save()
            comments_list = models.GroupComment.objects.filter(group_name__exact=in_name)
            in_group = models.Group.objects.get(name__exact=in_name)
            is_member = in_group.members.filter(email__exact=request.user.email)

            context = {
                'group': in_group,
                'userIsMember': is_member,
                'comments': comments_list,
                'is_student': request.user.is_student
            }
            return render(request, 'group.html', context)
        else:
            form = forms.GroupCommentForm()
    return render(request, 'group.html')

def deleteGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.delete()
        request.user.group_set.remove(in_group)
        request.user.save()
        groups_list = models.Group.objects.all()
        context = {
            'groups': groups_list,
        }
        return render(request, 'groups.html', context)
    return render(request, 'autherror.html')