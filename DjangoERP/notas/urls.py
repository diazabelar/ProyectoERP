from django.urls import path
from . import views

app_name = 'notas'

urlpatterns = [
    path('', views.index, name='index'),
    path('categorias/', views.categorias_list, name='categorias'),
    path('categorias/nueva/', views.categoria_create, name='categoria_create'),
    path('notas/nueva/', views.nota_create, name='nota_create'),
    path('notas/<int:pk>/', views.nota_detail, name='nota_detail'),
    path('notas/<int:pk>/editar/', views.nota_edit, name='nota_edit'),
]
