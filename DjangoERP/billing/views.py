from django.shortcuts import render
from .models import Customer

def list_customers(request):
    customers = Customer.objects.filter(company=request.company)
    return render(request, 'billing/customer_list.html', {'customers': customers})
