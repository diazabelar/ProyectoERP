from django.shortcuts import redirect
from django.urls import reverse, resolve
from core.models import Company
from django.http import HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate, login

class ActiveCompanyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow anonymous users to access the system with demo company - ALWAYS enable this
        if not request.user.is_authenticated:
            # Find demo company for anonymous users - prioritize "Pruevas"
            demo_company = Company.objects.filter(name="Pruevas").first()
            if not demo_company:
                demo_company = Company.objects.first()
            
            if demo_company:
                # Set company for anonymous users
                request.company = demo_company
                # Also store in session for consistency 
                request.session['demo_company_id'] = demo_company.id
            
            # Continue with the request - ALWAYS allow anonymous access
            return self.get_response(request)
        
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        public_urls = [
            reverse('login'),
            reverse('logout')
        ]
        
        # Add dashboard URLs to public_urls - we'll handle the company selection in the view
        if hasattr(request, '_current_scheme_host'):
            dashboard_url = request._current_scheme_host + reverse('dashboard')
            dashboard_alt_url = request._current_scheme_host + reverse('dashboard_alt')
            public_urls.extend([dashboard_url, dashboard_alt_url])
        
        # Safely determine admin URL path
        admin_path = '/admin/'

        if request.user.is_authenticated:
            active_company_id = request.session.get('active_company_id')

            # Always try to get a company for authenticated users
            if active_company_id:
                try:
                    company = Company.objects.get(pk=active_company_id)
                    if company in request.user.profile.authorized_companies.all():
                        request.company = company
                    else:
                        # If the user no longer has access to the company, select another one
                        first_company = request.user.profile.authorized_companies.first()
                        if first_company:
                            request.company = first_company
                            request.session['active_company_id'] = first_company.id
                        # Only redirect if not going to a public URL or admin
                        elif request.path not in public_urls and not request.path.startswith(admin_path):
                            return redirect('select_or_create_company')
                except Company.DoesNotExist:
                    # Auto-select first authorized company
                    first_company = request.user.profile.authorized_companies.first()
                    if first_company:
                        request.company = first_company
                        request.session['active_company_id'] = first_company.id
                    # Only redirect if not going to a public URL or admin
                    elif request.path not in public_urls and not request.path.startswith(admin_path):
                        return redirect('select_or_create_company')
            else:
                # Auto-select first authorized company
                first_company = request.user.profile.authorized_companies.first()
                if first_company:
                    request.company = first_company
                    request.session['active_company_id'] = first_company.id
                # Only redirect if not going to a public URL or admin
                elif request.path not in public_urls and not request.path.startswith(admin_path):
                    return redirect('select_or_create_company')

        response = self.get_response(request)
        return response


class GuestAccessMiddleware:
    """Automatically authenticates anonymous users as guest with access to 'Pruevas'"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only handle anonymous users and skip for admin and login pages
        if (not request.user.is_authenticated and 
            not request.path.startswith('/accounts/') and 
            not request.path.startswith('/admin/')):
            
            # Find the guest user or create one
            guest_user, created = User.objects.get_or_create(
                username='guest',
                defaults={
                    'email': 'guest@example.com',
                    'is_staff': False,
                    'is_superuser': False,
                    'first_name': 'Usuario',
                    'last_name': 'Invitado'
                }
            )
            
            if created:
                guest_user.set_unusable_password()
                guest_user.save()
            
            # Find Pruevas company
            pruevas_company = Company.objects.filter(name="Pruevas").first()
            
            # If company exists, assign it to the user and log them in
            if pruevas_company:
                # Make sure guest user has access to Pruevas
                if hasattr(guest_user, 'profile'):
                    if not guest_user.profile.authorized_companies.filter(pk=pruevas_company.id).exists():
                        guest_user.profile.authorized_companies.add(pruevas_company)
                
                # Auto-login the user without password
                request.user = guest_user
                
                # Set the session to remember this is a guest session
                request.session['is_guest_session'] = True
                request.session['active_company_id'] = pruevas_company.id
                
                # Assign the company to the request
                request.company = pruevas_company
        
        response = self.get_response(request)
        return response
