from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.index, name='index'),
    
    # Cliente URLs
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/create/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/', views.cliente_edit, name='cliente_edit'),
    path('clientes/<int:pk>/delete/', views.cliente_delete, name='cliente_delete'),
    path('clientes/<int:pk>/update/', views.cliente_update, name='cliente_update'),
    
    # Presupuesto URLs
    path('presupuestos/', views.presupuesto_list, name='presupuestos'),
    path('presupuestos/nuevo/', views.presupuesto_create, name='presupuesto_create'),
    path('presupuestos/<int:pk>/', views.presupuesto_edit, name='presupuesto_edit'),
    path('presupuestos/<int:pk>/eliminar/', views.presupuesto_delete, name='presupuesto_delete'),
    path('presupuestos/<int:pk>/linea/', views.presupuesto_add_line, name='presupuesto_add_line'),
    path('presupuestos/<int:pk>/linea/eliminar/', views.presupuesto_delete_line, name='presupuesto_delete_line'),
    
    # Factura URLs
    path('facturas/', views.facturas_list, name='facturas'),
    path('facturas/nueva/', views.factura_create, name='factura_create'),
]




