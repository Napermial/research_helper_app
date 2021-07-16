import simplejson
from django.shortcuts import render
from itertools import cycle
from .utils import pairwise
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from users import read_excel
from .models import Experiment, Item, Judgement, Level, Factor, ItemLevel


def index(request):
    """serves the homepage"""
    return render(request, "users/home.html")


@login_required
def experiments(request):
    """lists the users experiments with item counts and times they are filled"""
    users_experiments = Experiment.objects.filter(user_id=request.user.pk)
    items_count = []
    fill_count = []
    for experiment in users_experiments:
        item_count = Item.objects.filter(experiment_id=experiment.id).count()
        items_count.append(item_count)
        if item_count == 0:
            fill_count.append(0)
        else:
            fill = 0
            for item in Item.objects.filter(experiment_id=experiment.id):
                fill += Judgement.objects.filter(item_id=item.id).count()
            fill_count.append(fill)
    experiments_zipped = zip(users_experiments, items_count, fill_count)
    return render(request, "users/user.html", {'experiments': experiments_zipped})


@login_required
def create_experiment(request):
    """serves the experiment creator page"""
    return render(request, "users/create_experiment.html")


@login_required
def create_experiment_upload(request):
    """receives the excel file and loads the metadata to the database"""
    schema = simplejson.loads(request.POST['schema'])
    experiment = Experiment()
    experiment.name = request.POST['experiment_name']
    experiment.user_id = request.user
    experiment.save()
    file_name, file = request.FILES.popitem()
    levels = read_excel.insert_factors(schema, experiment)
    file_read, factor_positions = read_excel.read_file(file[0])
    read_excel.put_into_db(file_read, levels, experiment)
    return HttpResponseRedirect(f'/experiment/{experiment.pk}/edit')


@login_required
def edit_experiment(request, experiment_id):
    """lists the items of the experiment with the factors and items it belongs to"""
    exp = Experiment.objects.get(id=experiment_id)
    items = Item.objects.filter(experiment_id=experiment_id)
    item_level = ItemLevel.objects.filter(item__experiment_id=experiment_id)
    factors = Factor.objects.filter(experiment_id=experiment_id)
    levels = Level.objects.filter(factor__experiment_id=experiment_id)
    return render(request, "users/edit_experiment.html", {"experiment": exp, "items": items,
                                                          "levels": levels, "factors": factors,
                                                          "item_levels": item_level})


def view_experiment(request, experiment_id):
    """runs the experiment as a filler - displays the intro / item"""
    experiment = Experiment.objects.get(id=experiment_id)
    first_item = Item.objects.get(experiment_id=experiment_id)
    return render(request, "users/run_experiment.html", {"experiment": experiment, 'first_item': first_item})


def view_next_experiment_item(request, experiment_id, item_id):
    """gets the next item in the experiment to show"""
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
    """inserts the judgement of the filler to the database"""
    data = simplejson.loads(request.body)
    Judgement(judgement=data['judgement'], item_id=data['item_id']).save()
    return HttpResponse(b'success')


@require_POST
def delete_experiment(request):
    """deletes the experiment and all items, judgements, levels and factors"""
    data = simplejson.loads(request.body)
    Experiment.objects.get(id=data["experiment_id"]).delete()
    return HttpResponse(b'success')
