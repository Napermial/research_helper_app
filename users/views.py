from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, "users/home.html")


@login_required
def user(request, user_id):
    return render(request, "users/user.html")


@login_required
def researches(request):
    return render(request, "users/user.html", {'n': range(20)})


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user_auth = authenticate(request, username=username, password=password)
    if user_auth is not None:
        login(request, user)
    else:
        return HttpResponse('no')


def logout_view(request):
    logout(request)
    return HttpResponse('logged out')


def register(request):
    return HttpResponse('start')
