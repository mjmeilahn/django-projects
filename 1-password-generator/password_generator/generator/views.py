from django.shortcuts import render

# Create your views here.
def home (request):
    return render(request, 'generator/home.html', {'password': 'zs2308g2g0n'})

def password (request):
    return render(request, 'generator/password.html', {})
