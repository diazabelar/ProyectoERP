from django.urls import path
from . import views

app_name = 'contabilidad'  # This namespace is important for the 'contabilidad:cuentas_list' reference

urlpatterns = [
    path('', views.index, name='index'),
    path('cuentas/', views.cuentas_list, name='cuentas_list'),
    path('cuentas/nueva/', views.cuenta_create, name='cuenta_create'),
    path('cuentas/crear/', views.cuenta_create, name='cuenta_crear'),
    path('cuentas/<int:pk>/', views.cuenta_detail, name='cuenta_detail'),
    path('cuentas/editar/<int:pk>/', views.cuenta_update, name='cuenta_editar'),
    path('cuentas/eliminar/<int:pk>/', views.cuenta_delete, name='cuenta_eliminar'),
    path('asientos/', views.asientos_list, name='asientos_list'),
    path('asientos/nuevo/', views.asiento_create, name='asiento_create'),
    path('asientos/<int:pk>/', views.asiento_detail, name='asiento_detail'),
]
