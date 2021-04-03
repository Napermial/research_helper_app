from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "home.html", {})


@login_required
def user(request, user_id):
    response = "You're looking at the profile of user %s."
    return HttpResponse(response % user_id)


def register(request):
    return HttpResponse('start')


def login(request):
    return HttpResponse('start')


def logout(request):
    return HttpResponse('start')
