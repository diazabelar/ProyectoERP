from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.index, name='index'),
    path('citas/', views.citas, name='citas'),
    path('tareas/', views.tareas, name='tareas'),
    path('calendario/', views.calendario, name='calendario'),
    # Add other URL patterns as needed
]
