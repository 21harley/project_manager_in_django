from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'index.html')

def login_user(request):
    if request.method == 'GET':
        return render(request, 'Login.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['name'], password=request.POST['password'])
        if user is None:
            return render(request, 'Login.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('home')

def register_user(request):
    if request.method == 'GET':
        return render(request, 'Register.html', {"form": UserCreationForm, 'error':''})
    else:
            print(request.POST)
            try:
                user = User.objects.create_user(
                    request.POST["name"], password=request.POST["password"])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'Register.html', {"form": UserCreationForm, "error": "Username already exists."})

    return render(request, 'Register.html', {"form": UserCreationForm, "error": "Passwords did not match."})

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')