from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from core.models import Company  # Add this import

def dashboard(request):
    # For anonymous users, automatically select "Pruevas"
    if not request.user.is_authenticated:
        demo_company = Company.objects.filter(name="Pruevas").first()
        if not demo_company:
            # If "Pruevas" doesn't exist, get the first company
            demo_company = Company.objects.first()
        
        return render(request, 'dashboard.html', {
            'title': 'Panel de Control',
            'company': demo_company,
            'is_demo': True  # Flag to indicate demo mode
        })
    
    # Regular behavior for authenticated users
    return render(request, 'dashboard.html', {
        'title': 'Panel de Control',
    })

@login_required
def profile(request):
    return render(request, 'perfil/profile.html')
