from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('experiments', views.experiments, name='experiments'),
    path('auth/', include('django.contrib.auth.urls')),
    path('create/experiment', views.create_experiment, name="create_experiment"),
    path('create/experiment/upload', views.create_experiment_upload, name="create_experiment"),
    path('experiment/<int:experiment_id>/edit', views.edit_experiment, name="edit-experiment"),
    path('experiment/<int:experiment_id>', views.view_experiment, name="view-experiment"),
    path('experiment/<int:experiment_id>/<int:item_id>', views.view_next_experiment_item, name="nth-experiment-item"),
    path('experiment/submit', views.submit_judgement, name='submit-judgement'),
    path('experiments/delete', views.delete_experiment, name='delete-experiment')
]

