from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required as django_login_required
from functools import wraps
from core.models import Company
from django.contrib.auth import login
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

# Monkey-patch the login_required decorator to bypass checks for guest access
original_login_required = django_login_required

def patched_login_required(function=None, redirect_field_name=None, login_url=None):
    """
    Decorator that replaces the standard login_required to allow guest access
    """
    actual_decorator = original_login_required(function, redirect_field_name, login_url)
    
    @wraps(actual_decorator)
    def wrapper(request, *args, **kwargs):
        # Check if we're allowing guest access
        if hasattr(request, 'session') and request.session.get('guest_access'):
            # We have guest access, bypass login requirement
            if not request.user.is_authenticated:
                # Automatically set Pruevas company for guests
                demo_company = Company.objects.filter(name="Pruevas").first()
                if demo_company:
                    request.company = demo_company
            
            # Call the view function directly
            return function(request, *args, **kwargs)
        
        # Otherwise use the standard login required behavior
        return actual_decorator(request, *args, **kwargs)
    
    return wrapper

# Replace the standard Django login_required with our patched version
import django.contrib.auth.decorators
django.contrib.auth.decorators.login_required = patched_login_required
