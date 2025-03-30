from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.authorized_companies.exists():
            if 'active_company_id' in self.request.session:
                return reverse('landing')  # Ensure the correct URL name for the landing page
            else:
                # Redirect to select_company and let that view handle setting the session
                return reverse('select_company')
        else:
            return reverse('admin:index') # Or some other appropriate page

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            return redirect('select_company')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
