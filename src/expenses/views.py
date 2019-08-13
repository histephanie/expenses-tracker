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

    # by default, look at the current month
    selected_timeframe = datetime.now()

    # if a specific timeframe was requested, set our timeframe to that
    if month is not None:
        # get the month/year from the slug
        selected_timeframe = datetime.strptime(month, "%Y-%m").date()

    month_text = selected_timeframe.strftime('%B')
    current_month_slug = selected_timeframe.strftime('%Y-%m')
    # take selected date and replace it with the first day of that month
    # eg. Aug 13th, 2019 becomes Aug 1st, 2019
    first = selected_timeframe.replace(day=1)
    # take the first day of the month and subtract one more day
    # taking you back to the previous month
    prev_month = (first - timedelta(days=1)).strftime('%Y-%m')
    last = selected_timeframe.replace(day=28)
    next_month = (last + timedelta(days=4)).strftime('%Y-%m')

    year = selected_timeframe.strftime('%Y')
    month = selected_timeframe.strftime('%m')
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
        'prev_month': prev_month,
        'next_month': next_month,
    }
    return render(request, "expense-list.html", context)
