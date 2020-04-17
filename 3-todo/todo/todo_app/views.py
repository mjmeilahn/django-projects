from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm

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

# LOGIN
def login_user (request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', { 'form': AuthenticationForm() })
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'todo/login_user.html', { 'error': 'Username and password did not match', 'form': AuthenticationForm() })
        else:
            login(request, user)
            return redirect('current_todos')

# LOGOUT
def logout_user (request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

# DASHBOARD
def current_todos (request):
    return render(request, 'todo/current_todos.html')

def create_todo (request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', { 'form': TodoForm() })
    elif request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user

            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/create_todo.html', { 'error': 'Something went wrong. Please try again.', 'form': TodoForm() })