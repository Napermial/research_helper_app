from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, "users/home.html")


@login_required
def user(request):
    return render(request, "users/user.html")


@login_required
def experiments(request):
    return render(request, "users/user.html", {'n': range(20)})


@login_required
def create_experiment(request):
    return render(request, "users/create_experiment.html")


@login_required
def create_experiment_upload(request):
    file = request.FILES.getlist()
    print(file)
    print(str(request.body))
    return HttpResponse("ahhan")