import simplejson
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from users import read_excel
from .models import Experiment


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
    experiment =  Experiment()
    experiment.name = request.POST['experiment_name']

    file_name, file = request.FILES.popitem()
    schema, file_read = read_excel.handle_file(schema, file)
    read_excel.put_into_db(file_read, schema, experiment.pk)
    return HttpResponse("ahhan")
