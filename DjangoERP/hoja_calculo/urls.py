from django.urls import path
from . import views

app_name = 'hoja_calculo'

urlpatterns = [
    path('', views.index, name='index'),
    path('nueva/', views.nueva_hoja, name='nueva'),
    path('mis-hojas/', views.mis_hojas, name='mis_hojas'),
    path('importar/', views.importar, name='importar'),
    path('exportar/', views.exportar, name='exportar'),
    path('editar/<int:pk>/', views.editar_hoja, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_hoja, name='eliminar'),
]
