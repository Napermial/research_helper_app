from django.urls import path, include
from django.views.generic.base import RedirectView

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path(f'experiments/list', views.experiments, name='experiments'),
    path('api/public', views.public),
    path('api/private', views.private),
    path('api/private-scoped', views.private_scoped)
]

