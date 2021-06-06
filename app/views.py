from django.shortcuts import render,redirect
#from django.http import HttpResponse
from django.contrib import messages
from .models import *
from datetime import datetime, timedelta,date

# Create your views here.


def register(request):
    if request.method =='GET':
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for error in errors.values():
            messages.error(request, error)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        return redirect('/shows')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'],request.POST['password']):
        messages.error(request, 'Invalid Email / Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/shows')

def create(request):
    if request.method == "POST":
        errors = Show.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print(errors)
            return redirect("/shows/new")
        Show.objects.create(
            title =request.POST['title'],
            network = request.POST['network'],
            release_date = request.POST['release_date'],
            description = request.POST['description'],
            user=User.objects.get(id=request.session['user_id'])
        )
    return redirect("/shows")

def update(request,id):
    if request.method == "POST":
        errors = Show.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/shows/edit/{id}")
        else:
            show=Show.objects.get(id=id)
            show.title=request.POST['title']
            show.network=request.POST['network']
            show.release_date=request.POST['release_date']
            show.description=request.POST['description']
            show.save()
    return redirect('/shows')

def logout(request):
    request.session.clear()
    return redirect('/')


def delete(request,id):
    show=Show.objects.get(id=id)
    show.delete()
    return redirect("/shows")


#Render
def index(request):
    return render(request, 'index.html')


def shows(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    print(user)
    context = {
        'user': user,
        'user_shows':Show.objects.filter(user = user),
    }
    return render(request, 'shows.html', context)

def show(request, id):
    show=Show.objects.get(id=id)
    context={
        'show':Show.objects.get(id=id)
    }
    return render(request,"show.html",context)

def edit(request,id):
    context={
        'show':Show.objects.get(id=id)
    }
    return render(request,"edit.html",context)

def new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'new.html', context)