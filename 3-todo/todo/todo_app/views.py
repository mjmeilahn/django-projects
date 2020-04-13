from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def signup_user (request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', { 'form': UserCreationForm() })
    elif request.method == 'POST':
        password = request.POST['password1']

        if password == request.POST['password2']:
            user = User.objects.create_user(request.POST['username'], password=password)

            user.save()
        else:
            # TELL USER TO MATCH PASSWORD
            print('Please match passwords for new user')