from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    path('', views.index, name='index'),
    
    # Provider URLs
    path('proveedores/', views.proveedores_list, name='proveedores'),
    path('proveedores/nuevo/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/', views.proveedor_detail, name='proveedor_detail'),
    path('proveedores/<int:pk>/editar/', views.proveedor_edit, name='proveedor_update'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_delete, name='proveedor_delete'),
    
    # Purchase Orders URLs (Órdenes de Compra)
    path('compras/', views.compras_list, name='compras'),
    path('compras/nueva/', views.compra_create, name='compra_create'),
    path('compras/<int:pk>/', views.compra_detail, name='compra_detail'),
    path('compras/<int:pk>/editar/', views.compra_edit, name='compra_update'),
    path('compras/<int:pk>/eliminar/', views.compra_delete, name='compra_delete'),
    
    path('facturas/', views.facturas, name='facturas'),
    path('facturas/nueva/', views.factura_create, name='factura_create'),
]
