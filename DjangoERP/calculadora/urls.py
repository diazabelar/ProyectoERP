from django.urls import path
from . import views

app_name = 'calculadora'

urlpatterns = [
    path('', views.index, name='index'),
    path('financiera/', views.financiera, name='financiera'),
    path('divisas/', views.divisas, name='divisas'),
    path('impuestos/', views.impuestos, name='impuestos'),
    # Add other URL patterns as needed
]
