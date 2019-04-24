# chat/views.py
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from chat.models import *
from django.contrib import messages
import json

def index(request):
    return render(request, 'chat/index.html', {})

def login_and_registration(request):
    return render(request, 'chat/login_and_registration.html')

def register(request):
    if request.method=="POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key in errors:
                messages.error(request, errors[key])
            return redirect("/")
        else:
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name = request.POST["first_name"], last_name = request.POST["last_name"], email = request.POST["email"], password = password)
            request.session['id'] = new_user.id
            request.session['email'] = request.POST['email']
            return redirect('/chat/') 
    return redirect('/')

def login(request):
    if request.method=="POST":
        errors = User.objects.validate_login(request.POST)
        if len(errors) > 0:
            for key in errors:
                messages.error(request, errors[key])
            return redirect("/")
        else:
            user_logged_in = User.objects.get(email=request.POST["email_login"])
            request.session["id"] = user_logged_in.id
            request.session['email'] = request.POST['email_login']
            return redirect('/chat/')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect("/") 

def room(request, room_name):
    this_email = request.session['email']
    print('this is: ~~', this_email)
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'this_email_json': mark_safe(json.dumps(this_email)),
    })