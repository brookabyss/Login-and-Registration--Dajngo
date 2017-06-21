from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
from django.contrib import messages
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
    def birthday_check(self, birthday):
        # you have to be at least a day old to register
        current_date=datetime.now()-timedelta(days=1)
        print "Date time now", datetime.now()
        print"Current date #$^$%^$%^", current_date
        if birthday < current_date:
            return True
        else:
            return False


    def registration(self,request):
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        if len(request.POST['birthday'])>0:
            birthday=datetime.strptime(request.POST['birthday'],'%Y-%m-%d')
        else:
            messages.error(request,"Birthday field is not filled")
            return False
        print "Birthday: ", birthday
        password=request.POST['password']
        c_password=request.POST['confirm']
        error_count=0
        #check for first_name
        if not self.check_length(first_name):
            error_count+=1
            messages.error(request,"The length of first name can't be less than two charcters.", 'first_name')
        #check for last_name
        if not self.check_length(last_name):
            error_count+=1
            messages.error(request,"The length of last name can't be less than two charcters.",'last_name')
        #check email
        if not self.check_email(email):
            error_count+=1
            messages.error(request,"Email invalid",'email')
        # Check password
        if not self.check_password_length(password):
            error_count+=1
            messages.error(request,"Password too short!",'password')
        if not self.confirm_password(password,c_password):
            error_count+=1
            messages.error(request,"Passwords don't match",'c_password')
        if not self.birthday_check(birthday):
            error_count+=1
            messages.error(request,"You have to be at least a day old to register",'birtdhay')
        print "Messages"*10,messages

        if error_count<1:
            self.create(first_name=first_name,last_name=last_name,email=email,password=password)
            return True
        else:
            return False


    def login(self,request):
        email=request.POST['email']
        password=request.POST['password']
        users=self.filter(email=email)
        if users.count()< 1:
            messages.error(request,"Your email address is not registered, please register",'login')
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
    birthday=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    def __str__(self):
        return self.first_name +" "+self.last_name
