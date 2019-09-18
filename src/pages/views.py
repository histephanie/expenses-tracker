from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from bs4 import BeautifulSoup
from django.http import HttpResponse
from datetime import datetime
from expenses.models import Expense, User

# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        # can_reg = True
        email = form.data.get('email')
        if User.objects.filter(email=email).count() > 0:
            form.add_error("email", "Email address must be unique")


        # FIND IF A USER WITH `email` EXISTS
        # IF IT DOES, dont proceed with reg
        # if email exists in db:
        #     can_reg = false
        if form.is_valid(): # and can_reg:
            form.save() # saves the user to db
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('expenses')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def test_parse_email(*args, **kwargs):

    sender = "stephanie.bogantes@gmail.com"
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
        store = store.replace('Продажба', '')
        #remove spaces around string (leading and trailing whitespace char)
        store = store.strip()
        #replace the unicode non-breaking space with a regular space
        store = store.replace(u'\xa0', " ")

        amount = tds[3].text
        amount = amount.strip()
        amount = amount.replace('.', '')
        amount = amount.replace(',', '.')
        amount = float(amount)

        sender_user = User.objects.get(email=sender)
        print(type(sender_user)) # THIS MUST BE: User

        expense = Expense(store=store, date=date, amount=amount, user=sender_user)
        expense.save()

        expense = {"date":date, "store":store, "amount":amount}
        expenses.append(expense)
    print(expenses)

    return HttpResponse("hello")

    #check the email address sent by mailgun and assign the
    #expenses to the user with the same email address
