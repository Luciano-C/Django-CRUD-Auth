from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


# Create your views here.
def home(request):
    return render(request, "home.html", {
        "form": UserCreationForm
    })


def signup(request):

    if request.method == "GET":
        return render(request, "signup.html", {
            "form": UserCreationForm
        })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # register user
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                # Actualiza las cookies de inicio de sesión
                login(request, user)
                # Usamos el nombre <=> path('tasks/', views.tasks, name='tasks') de urls.py
                return redirect('tasks')
            # Se pueden listar except para diferentes tipos de error.
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": 'Username already exists'
                })

        return render(request, "signup.html", {
            "form": UserCreationForm,
            "error": 'Passwords do not match'
        })


def tasks(request):
    return render(request, 'tasks.html')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

