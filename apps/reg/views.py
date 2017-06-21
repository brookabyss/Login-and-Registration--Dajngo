from django.shortcuts import render, redirect
from .models import Users
from django.contrib import messages

def index(request):
    return render(request,'reg/index.html')

def register(request):
    if request.method=="POST":
        #if the fields pass the vaildation the  object will be created in the database
        if Users.objects.registration(request):
            context={
                'name':request.POST['first_name'],
                'action': "registered"
            }
            messages.success(request,'Successfully registered')
            return render(request,'reg/show.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def login(request):

    if request.method=="POST":
        login=Users.objects.login(request)
        if login==False:
            return redirect('/')
        else:
            context={
                'name': login.first_name,
                'action': "logged in"
            }
            messages.success(request,'Successfully logged in')
            return render(request,'reg/show.html', context)

    else:
        return redirect('/')
