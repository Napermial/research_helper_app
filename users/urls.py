from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('research', views.experiments, name='research'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('auth/', include('django.contrib.auth.urls')),
    path('create/experiment', views.create_experiment, name="create_experiment"),
    path('create/experiment/upload', views.create_experiment_upload, name="create_experiment"),
]
