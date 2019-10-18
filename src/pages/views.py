from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.http import HttpResponse
from datetime import datetime
from expenses.models import Expense, User

# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        email = form.data.get('email')
        if User.objects.filter(email=email).count() > 0:
            form.add_error("email", "Email address must be unique")

        if form.is_valid():
            form.save() # saves the user to db
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('expenses')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
