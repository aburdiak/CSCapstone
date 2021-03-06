# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 12:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=120, null=True)),
                ('last_name', models.CharField(blank=True, max_length=120, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_professor', models.BooleanField(default=False)),
                ('is_engineer', models.BooleanField(default=False)),
                ('needs_university', models.BooleanField(default=False)),
                ('needs_company', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('alma_mater', models.CharField(blank=True, default='No alma mater', max_length=120)),
                ('company', models.CharField(blank=True, default='No company', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.CharField(blank=True, default='No phone number', max_length=120)),
                ('university', models.CharField(blank=True, default='No university', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('grad_year', models.CharField(blank=True, default='No grad year', max_length=120)),
                ('university', models.CharField(blank=True, default='No university', max_length=120)),
            ],
        ),
    ]
