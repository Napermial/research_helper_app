import simplejson
from django.shortcuts import render
from itertools import cycle
from .utils import pairwise
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from users import read_excel
from .models import Experiment, Item, Judgement, Level, Factor


def index(request):
    return render(request, "users/home.html")


@login_required
def user(request):
    return render(request, "users/user.html")


@login_required
def experiments(request):
    users_experiments = Experiment.objects.filter(user_id=request.user.pk)
    items_count = []
    fill_count = []
    for experiment in users_experiments:
        item_count = Item.objects.filter(experiment=experiment.id).count()
        items_count.append(item_count)
        if item_count == 0:
            fill_count.append(0)
        else:
            fill = 0
            for item in Item.objects.filter(experiment_id=experiment.id):
                fill += Judgement.objects.filter(item_id=item.id).count()
            fill_count.append(fill)
    print(fill_count)
    print(items_count)
    print(users_experiments)
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
    experiment.user_id = request.user
    experiment.save()
    file_name, file = request.FILES.popitem()
    read_excel.insert_factors(schema, experiment.pk)
    schema, file_read = read_excel.handle_file(schema, file)
    read_excel.put_into_db(file_read, schema, experiment)
    return HttpResponseRedirect(f'/experiment/{experiment.pk}/edit')


@login_required
def edit_experiment(request, experiment_id):
    exp = Experiment.objects.get(id=experiment_id)
    items = Item.objects.filter(experiment_id=experiment_id)
    levels = Level.objects.filter(experiment_id=experiment_id)
    return render(request, "users/edit_experiment.html", {"experiment": exp, "items": items, "levels": levels})


def view_experiment(request, experiment_id):
    experiment = Experiment.objects.get(id=experiment_id)
    first_item = Item.objects.filter(experiment_id=experiment_id).first()
    return render(request, "users/run_experiment.html", {"experiment": experiment, 'first_item': first_item})


def view_next_experiment_item(request, experiment_id, item_id):
    experiment = Experiment.objects.get(id=experiment_id)
    items = Item.objects.filter(experiment_id=experiment_id)
    for elem, next_elem in pairwise(cycle(items)):
        if elem.id == item_id:
            item = next_elem
            break
    else:
        item = {}
    return render(request, "users/run_experiment.html", {"experiment": experiment, 'item': item})


@require_POST
def submit_judgement(request):
    data = simplejson.loads(request.body)
    Judgement(judgement=data['judgement'], item_id=data['item_id']).save()
    return HttpResponse(b'success')
