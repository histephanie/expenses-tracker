from django.shortcuts import render, redirect
from .models import Expense

# Create your views here.

# This view shows a list of all expenses made by the user in the current month
# unless a specific month was requested
def expense_list_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')

    expenses = Expense.objects.filter(user=request.user)
    print(expenses)
    context = { 'expenses': expenses}
    return render(request, "expense-list.html", context)

# def categorize_view():
