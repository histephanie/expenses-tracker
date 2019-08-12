from django.shortcuts import render, redirect
from .models import Expense, ExpenseCategory
from datetime import datetime, date, timedelta


# Create your views here.

# This view shows a list of all expenses made by the user in the current month
# unless a specific month was requested
def expense_list_view(request, month=None):
    # verify if user is logged in, otherwise redirect to log in page
    if not request.user.is_authenticated:
        return redirect('login')

    current_date = datetime.now()
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    month_text = datetime.now().strftime('%B')
    current_month_slug = datetime.now().strftime('%b-%Y')

    if month is not None:
        # Get the month/year from the slug
        current_date = # parse the slug

    today = current_date.today()
    first = today.replace(day=1)
    last_month = (first - timedelta(days=1)).strftime('%b-%Y')


    expenses = Expense.objects.filter(user=request.user, date__year=year, date__month=month)

    # get all categories from the database
    cats = ExpenseCategory.objects.all()
    # make an empty dict and at index category wich is an id from the database,
    # assing the value of a dict containing category name and an empty list for expenses
    categories = {}
    for category in cats:
        categories[category] = {'name': category.name, 'expenses': []}

    # for each expense, find it's category, and in the categories dictionary
    # at key of the current expense's category, add itself to the expenses key
    for expense in expenses:
        categories[expense.category]['expenses'].append(expense)

    context = {
        'categories': categories,
        'current_month_text': month_text,
        'current_month_slug': current_month_slug,
        'last_month': last_month,
    }
    return render(request, "expense-list.html", context)
