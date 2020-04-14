from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db import IntegrityError

# HOME
def home (request):
    return render(request, 'todo/home.html')

# SIGN UP
def signup_user (request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', { 'form': UserCreationForm() })
    elif request.method == 'POST':
        password = request.POST['password1']

        if password == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=password)

                # SAVE USER TO DB
                user.save()

                # LOG IN USER
                login(request, user)

                # REDIRECT TO DASHBOARD
                return redirect('current_todos')

            # SUBMITTED DATA ENCOUNTERS AN ERROR AGAINST DB RECORDS
            except IntegrityError:
                return render(request, 'todo/signup_user.html', { 'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose another username.' })
        # PASSWORDS DID NOT MATCH
        else:
            return render(request, 'todo/signup_user.html', { 'form': UserCreationForm(), 'error': 'Passwords did not match' })

# LOGOUT
def logout_user (request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

# DASHBOARD
def current_todos (request):
    return render(request, 'todo/current_todos.html')