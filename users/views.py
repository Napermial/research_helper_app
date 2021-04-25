import simplejson
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from users import read_excel


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
    schema = simplejson.loads(request.POST['schema'])
    print(schema)
    file_name, file = request.FILES.popitem()
    read_excel.handle_file(schema, file_name, file)
    return HttpResponse("ahhan")
