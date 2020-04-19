from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from .models import Todo


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
@login_required
def logout_user (request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


# VIEW ALL TODOS
@login_required
def current_todos (request):
    todos = Todo.objects.filter(user = request.user, date_completed__isnull = True)
    return render(request, 'todo/current_todos.html', { 'todos': todos })

# VIEW ALL COMPLETED TODOS
@login_required
def completed_todos (request):
    todos = Todo.objects.filter(user = request.user, date_completed__isnull = False).order_by('-date_completed')
    return render(request, 'todo/completed_todos.html', { 'todos': todos })


# VIEW TODO
@login_required
def todo (request, todo_pk):
    todo = get_object_or_404(Todo, pk = todo_pk, user = request.user)

    if request.method == 'GET':
        form = TodoForm(instance = todo)
        return render(request, 'todo/todo.html', { 'todo': todo, 'form': form })
    elif request.method == 'POST':
        try:
            form = TodoForm(request.POST, instance = todo)
            form.save()
            return redirect('current_todos')
        except (ValueError, IntegrityError):
            return render(request, 'todo/todo.html', { 'todo': todo, 'form': form, 'message': 'Something went wrong. Please try again.' })


# CREATE TODO
@login_required
def create_todo (request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', { 'form': TodoForm() })
    elif request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit = False)
            new_todo.user = request.user

            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/create_todo.html', { 'error': 'Something went wrong. Please try again.', 'form': TodoForm() })


# COMPLETE TODO
@login_required
def complete_todo (request, todo_pk):
    todo = get_object_or_404(Todo, pk = todo_pk, user = request.user)

    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('current_todos')

# DELETE TODO
@login_required
def delete_todo (request, todo_pk):
    todo = get_object_or_404(Todo, pk = todo_pk, user = request.user)

    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')