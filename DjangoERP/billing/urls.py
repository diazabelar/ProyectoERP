from django.urls import path
from . import views

app_name = 'billing'  # Add this line
urlpatterns = [
    path('customers/', views.list_customers, name='customer_list'),
]
