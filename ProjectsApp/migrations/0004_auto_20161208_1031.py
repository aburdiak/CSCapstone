# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 10:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsApp', '0003_remove_project_group_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='company',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='project',
            name='experience',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='project',
            name='language',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='project',
            name='speciality',
            field=models.CharField(max_length=200),
        ),
    ]
