from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from bs4 import BeautifulSoup
from django.http import HttpResponse
from datetime import datetime


# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('expenses')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def test_parse_email(*args, **kwargs):

    mytxt = 'email.html'
    soup = BeautifulSoup(open(mytxt), 'html.parser')
    expenses = []
    trs = soup.findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        # ignores trs that dont contain tds
        # such as the table header
        if len(tds) < 4:
            continue

        date = tds[0].text
        try:
            date = datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            continue

        store = tds[1].text
        amount = tds[3].text

        expense = {"date":date, "store":store, "amount":amount}
        expenses.append(expense)
    print(expenses)

    return HttpResponse("hello")
