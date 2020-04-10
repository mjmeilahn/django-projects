# from django.http import HttpResponse
from django.shortcuts import render
import random

# Create your views here.
def home (request):
    return render(request, 'generator/home.html')

def about (request):
    return render(request, 'generator/about.html')

def password (request):
    password = ''
    characters = list('abcdefghijklmnopqrstuvwxyz')
    length = int(request.GET.get('length', 12))

    # ADD UPPERCASE TO LIST
    if request.GET.get('uppercase'):
        characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    # ADD SPECIAL CHARACTERS TO LIST
    if request.GET.get('special_chars'):
        characters.extend(list('!@#$%^&*()'))

    # ADD NUMBERS TO LIST
    if request.GET.get('numbers'):
        characters.extend(list('0123456789'))

    for i in range(length):
        password += random.choice(characters)

    return render(request, 'generator/password.html', {'password': password})
