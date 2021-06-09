from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('experiments', views.experiments, name='experiments'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('auth/', include('django.contrib.auth.urls')),
    path('create/experiment', views.create_experiment, name="create_experiment"),
    path('create/experiment/upload', views.create_experiment_upload, name="create_experiment"),
    path('experiment/<int:experiment_id>/edit', views.edit_experiment, name="edit-experiment"),
    path('experiment/<int:experiment_id>', views.view_experiment, name="view-experiment")
]
