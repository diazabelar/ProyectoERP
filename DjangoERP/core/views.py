from django.shortcuts import render, redirect
from core.models import Company
import logging
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CompanyForm  # Import the CompanyForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

@login_required
def select_or_create_company_view(request):
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        if company_id:
            request.session['active_company_id'] = company_id
            return redirect('dashboard')
        else:
            # Handle the case where no company_id is selected
            return render(request, 'core/select_or_create_company.html', {'error': 'Please select a company.'})
    else:
        companies = request.user.profile.authorized_companies.all()  # Fixed: Use profile.authorized_companies
        return render(request, 'core/select_or_create_company.html', {'companies': companies})

@login_required
def create_company_view(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            new_company = form.save()
            request.user.profile.authorized_companies.add(new_company)  # Fixed: Use profile.authorized_companies
            request.session['active_company_id'] = new_company.id
            return redirect('dashboard')
    else:
        form = CompanyForm()
    return render(request, 'core/create_company.html', {'form': form})

@login_required
@require_http_methods(["GET"])
def get_default_company(request):
    """API endpoint to get or set a default company for the current user"""
    if request.user.is_authenticated:
        # Check if there's already a company in session
        active_company_id = request.session.get('active_company_id')
        
        if active_company_id:
            try:
                company = Company.objects.get(pk=active_company_id)
                if company in request.user.profile.authorized_companies.all():
                    return JsonResponse({
                        'success': True,
                        'company_id': company.id,
                        'company_name': company.name
                    })
            except Company.DoesNotExist:
                pass
        
        # If no valid company in session, get the first authorized company
        first_company = request.user.profile.authorized_companies.first()
        if first_company:
            request.session['active_company_id'] = first_company.id
            return JsonResponse({
                'success': True,
                'company_id': first_company.id,
                'company_name': first_company.name
            })
    
    # No company available
    return JsonResponse({
        'success': False,
        'message': 'No company available'
    })

def homepage_view(request):
    """Homepage view that is visible to all users"""
    context = {}
    
    # If the user is authenticated, add company info
    if request.user.is_authenticated:
        company = getattr(request, 'company', None)
        context['company'] = company
        context['is_authenticated'] = True
    else:
        context['is_authenticated'] = False
    
    # Use the main dashboard template
    return render(request, 'dashboard.html', context)  # This will use /home/abe/ERPDJANGO/DjangoERP/templates/dashboard.html
