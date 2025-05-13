from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import BusinessSignUpForm

def dashboard(request):
    return render(request, 'users/dashboard.html')

def signup_view(request):
    if request.method == 'POST':
        form = BusinessSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tableTapApp:menu_management')
    else:
        form = BusinessSignUpForm()
    return render(request, 'registration/sign_up.html', {'form': form})