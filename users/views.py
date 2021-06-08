import simplejson
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from users import read_excel
from .models import Experiment, Item, Judgement


def index(request):
    return render(request, "users/home.html")


@login_required
def user(request):
    return render(request, "users/user.html")


@login_required
def experiments(request):
    users_experiments = Experiment.objects.all()
    items_count = [Item.objects.filter(experiment=experiment.id).count() for experiment in users_experiments]
    fill_count = [Judgement.objects.filter(item_id=item).count() for item in items_count]
    experiments_zipped = zip(users_experiments, items_count, fill_count)
    return render(request, "users/user.html", {'experiments': experiments_zipped})


@login_required
def create_experiment(request):
    return render(request, "users/create_experiment.html")


@login_required
def create_experiment_upload(request):
    schema = simplejson.loads(request.POST['schema'])
    experiment = Experiment()
    experiment.name = request.POST['experiment_name']
    experiment.save()
    file_name, file = request.FILES.popitem()
    schema, file_read = read_excel.handle_file(schema, file)
    read_excel.put_into_db(file_read, schema, experiment)
    return HttpResponseRedirect(f'/experiment/{experiment.pk}/edit')


@login_required
def edit_experiment(request, experiment_id):
    return render(request, "users/edit_experiment.html")


@login_required
def view_experiment(request, experiment_id):
    return render(request, "users/edit_experiment.html")
