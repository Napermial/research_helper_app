import simplejson
from django.shortcuts import render
from itertools import cycle
from .utils import pairwise, jwt_get_username_from_payload_handler, jwt_decode_token, get_user_from_token
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from functools import wraps
import jwt

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from users import read_excel
from .models import Experiment, Item, Judgement, Level, Factor, ItemLevel, Intro, SentenceOrder, \
    SentenceOrderConfiguration


def index(request):
    """serves the homepage"""
    return JsonResponse({"message": "hello"})


@permission_classes([IsAuthenticated])
def experiments(request):
    """lists the users experiments with item counts and times they are filled"""
    token = request.headers.get('Authorization')
    if token is None:
        return HttpResponse("You need to log in to access this resource", status=403)
    decoded = jwt_decode_token(token.replace("Bearer ", ""))
    user = get_user_from_token(decoded)
    users_experiments = Experiment.objects.filter(user_id=user.pk)
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
    json_experiments = {}
    for experiment, item, fill in zip(users_experiments, items_count, fill_count):
        json_experiments[experiment] = [item, fill]
    return JsonResponse(json_experiments)


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
    intros = Intro.objects.filter(experiment=exp)
    items = Item.objects.filter(experiment_id=experiment_id)
    item_level = ItemLevel.objects.filter(item__experiment_id=experiment_id)
    factors = Factor.objects.filter(experiment_id=experiment_id)
    levels = Level.objects.filter(factor__experiment_id=experiment_id)
    return render(request, "users/edit_experiment.html", {"experiment": exp, "items": items,
                                                          "levels": levels, "factors": factors,
                                                          "item_levels": item_level,
                                                          "intros": intros})


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


def order_items(request, experiment_id):
    """lets the user choose from the default orders and change sentences"""
    exp = Experiment.objects.get(id=experiment_id)
    intros = Intro.objects.filter(experiment=exp)
    items = Item.objects.filter(experiment_id=experiment_id)
    item_level = ItemLevel.objects.filter(item__experiment_id=experiment_id)
    factors = Factor.objects.filter(experiment_id=experiment_id)
    levels = Level.objects.filter(factor__experiment_id=experiment_id)
    return render(request, "users/order_experiments.html", {"experiment": exp, "items": items,
                                                            "levels": levels, "factors": factors,
                                                            "item_levels": item_level,
                                                            "intros": intros})


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


@require_POST
@login_required
def save_item_order(request, experiment_id):
    """gets a list of items and creates an order config from it"""
    data = simplejson.loads(request.body)
    conf_name = data[0]
    configuration = SentenceOrderConfiguration(configuration_name=conf_name, experiment_id=experiment_id,
                                               user=request.user.pk)
    for i, item in enumerate(data[1:-1]):
        if i == 0:
            configuration.first_sentence_id = item
            configuration.save()
        SentenceOrder(sentence_id=item, next_sentence_id=data[i + 1]).save()
    return HttpResponse(b'success')


@require_POST
@login_required
def save_changed_level(request):
    """changes the item of the experiment with the level given"""
    data = simplejson.loads(request.body)
    item_level = ItemLevel.objects.get(item_id=data["itemId"], level_id=data["previousLevel"])
    item_level.level = Level.objects.get(id=data["newLevel"])
    item_level.save()
    return HttpResponse()


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """

    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response

        return decorated

    return require_scope


@api_view(['GET'])
@permission_classes([AllowAny])
def public(request):
    return JsonResponse({'message': 'Hello from a public endpoint! You don\'t need to be authenticated to see this.'})


@api_view(['GET'])
def private(request):
    return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated to see this.'})


@api_view(['GET'])
@requires_scope('read:messages')
def private_scoped(request):
    return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated and have a scope '
                                    'of read:messages to see this.'})
