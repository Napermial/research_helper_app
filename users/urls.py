from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('research', views.researches, name='research'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('auth/', include('django.contrib.auth.urls')),
]
