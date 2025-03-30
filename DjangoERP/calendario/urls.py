from django.urls import path
from . import views

app_name = 'calendario'

urlpatterns = [
    path('', views.index, name='index'),
    path('mensual/', views.vista_mensual, name='vista_mensual'),
    path('eventos/', views.eventos, name='eventos'),
    path('sincronizacion/', views.sincronizacion, name='sincronizacion'),
    # Add other URL patterns as needed
]
