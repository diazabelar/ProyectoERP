from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('profile/', login_required(TemplateView.as_view(template_name='accounts/profile.html')), name='profile'),
]
