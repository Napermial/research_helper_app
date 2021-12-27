from django.urls import path, include
from django.views.generic.base import RedirectView

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path(f'experiments/list', views.experiments, name='experiments'),
    path(f"experiment/<experiment_id>/items", views.one_experiment),
]

