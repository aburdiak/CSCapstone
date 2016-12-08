"""GroupsApp URL

Created by Naman Patwari on 10/10/2016.
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^group/all$', views.getGroups, name='Groups'),
    url(r'^group/form$', views.getGroupForm, name='GroupForm'),
    url(r'^group/formsuccess$', views.getGroupFormSuccess, name='GroupFormSuccess'),
    url(r'^group/join$', views.joinGroup, name='GJoin'),
    url(r'^group/unjoin$', views.unjoinGroup, name='GUnjoin'),
    url(r'^group/addcomment$', views.addComment, name='CommentSend'),
    url(r'^group/adduser$', views.addUserByEmail, name='UserAdd'),
    url(r'^group/deletegroup$', views.deleteGroup, name='DeleteGroup'),
    url(r'^group$', views.getGroup, name='Group'),
]