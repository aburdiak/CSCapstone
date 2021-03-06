"""AuthenticationApp Models

Created by Naman Patwari on 10/4/2016.
"""

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, first_name=None, last_name=None, is_student=False,
                    is_professor=False, is_engineer=False, needs_university=False, needs_company=False):
        if not email:
            raise ValueError('Users must have an email address')
        print "In create user"
        print first_name
        print last_name
        #We can safetly create the user
        #Only the email field is required
        user = self.model(email=email)
        user.set_password(password)

        user.first_name = first_name
        user.last_name = last_name
        user.is_student = is_student
        user.is_professor = is_professor
        user.is_engineer = is_engineer
        user.needs_university = needs_university
        user.needs_company = needs_company
		

        #If first_name is not present, set it as email's username by default
        if first_name is None or first_name == "" or first_name == '':                                
            user.first_name = email[:email.find("@")]            

        user.save(using=self._db)
        print "End of create user"
        print first_name
        return user

    def create_superuser(self, email=None, password=None, first_name=None, last_name=None):
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        )

    last_name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        )

    is_active = models.BooleanField(default=True,)
    is_admin = models.BooleanField(default=False,)

    # #New fields added
    is_student = models.BooleanField(default=False,)
    is_professor = models.BooleanField(default=False,)
    is_engineer = models.BooleanField(default=False,)
    needs_university = models.BooleanField(default=False,)
    needs_company = models.BooleanField(default=False, )

    photo = models.ImageField(
        upload_to="static/images",
	default=0,
	)


  

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):        
        return "%s %s" %(self.first_name, self.last_name)

    def get_short_name(self):        
        return self.first_name

    def __str__(self):              #Python 3
        return self.email

    def __unicode__(self):           # Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):        
        return True

    def get_role(self):
        if self.is_student == True:
            return 'student'
        elif self.is_professor == True:
            return 'professor'
        elif self.is_engineer == True:
            return 'engineer'

    def get_email(self):
        return self.email


    @property
    def is_staff(self):
        return self.is_admin
    
#     def new_user_reciever(sender, instance, created, *args, **kwargs):
#     	if created:   
     
# Going to use signals to send emails
# post_save.connect(new_user_reciever, sender=MyUser)
             

class Student(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        primary_key=True)

    grad_year = models.CharField(
        max_length=120,
        default="No grad year",
        blank=True,
        )

    university = models.CharField(
        max_length=120,
        default="No university",
        blank=True,
        )

    def get_full_name(self):        
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):        
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):        
        return True


    @property
    def is_staff(self):
        return False

class Professor(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        primary_key=True)


    phone_number = models.CharField(
        max_length=120,
        default="No phone number",
        blank=True,
    )

    university = models.CharField(
        max_length=120,
        default="No university",
        blank=True,
        )


    


    def get_full_name(self):
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return True

class Engineer(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        primary_key=True)

    alma_mater = models.CharField(
        max_length=120,
        default="No alma mater",
        blank=True,
        )

    company = models.CharField(
        max_length=120,
        default="No company",
        blank=True,
        )


    def get_full_name(self):
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return False
