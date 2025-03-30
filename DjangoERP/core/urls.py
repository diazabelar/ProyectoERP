from django.urls import path
from . import views
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    # Use the appropriate dashboard directly as home
    path('', views.homepage_view, name='home'),  
    path('landing/', TemplateView.as_view(template_name='landing.html'), name='landing'),
    # Keep the dashboard path but point to the same view as home
    path('dashboard/', views.homepage_view, name='dashboard'),  
    path('seleccionar-o-crear-empresa/', views.select_or_create_company_view, name='select_or_create_company'),
    path('core/crear-empresa/', views.create_company_view, name='create_company'),
    # Add this new API endpoint
    path('api/get-default-company/', views.get_default_company, name='get_default_company'),
]
