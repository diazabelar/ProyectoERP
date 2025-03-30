from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.index, name='index'),  # Añadimos esta URL 
    path('lista/', views.lista_productos, name='lista_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('detalle/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
]
