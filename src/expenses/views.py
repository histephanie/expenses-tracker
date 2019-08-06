from django.shortcuts import render
from .models import Expense

# Create your views here.
def expense_list_view(request, *args, **kwargs):
    queryset = Expense.objects.all()
    context = { 'expenses':queryset}
    return render(request, "expense-list.html", context)
