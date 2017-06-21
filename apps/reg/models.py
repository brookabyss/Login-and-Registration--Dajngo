from __future__ import unicode_literals

from django.db import models
import re

class UserManager(models.Manager):

    def check_length(self,postData):
        if len(postData) < 2:
            return False
        else:
            return True

    def check_email(self,postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData):
            return False
        else:
            return True
    def check_password_length(self,password):
        if len(password) <8:
                return False
        else:
                return True
    def confirm_password(self,password,c_password):
        if password!=c_password:
                return False
        else:
                return True
    def registration(self,request):
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        c_password=request.POST['confirm']
        if 'errors' not in request.session.keys():
            request.session['errors']=[]
        #check for first_name
        if not self.check_length(first_name):
            request.session['errors'].append(['first_name',"The length of a name can't be less than two charcters."])
        #check for last_name
        if not self.check_length(last_name):
            request.session['errors'].append(['last_name',"The length of a name can't be less than two charcters."])
        #check email
        if not self.check_email(email):
            request.session['errors'].append(['email',"Email invalid"])
        # Check password
        if not self.check_password_length(password):
            request.session['errors'].append(['password',"Password too short!"])
        if not self.confirm_password(password,c_password):
            request.session['errors'].append(['c_password',"Passwords don't match"])


        if len(request.session['errors'])<1:
            self.create(first_name=first_name,last_name=last_name,email=email,password=password)
            return True
        else:
            return False


        def login(self,request):
            email=request.POST['email']
            password=request.POST['password']
            users=self.filter(email=email)
            if users.count()< 1:
                request.session['error'].append(['login',"Your email address is not registered, please register"])
                return False
            else:
                for user in users:
                    if password==user.password:
                        return user
                return False






class Users(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    def __str__(self):
        return self.first_name +" "+self.last_name
