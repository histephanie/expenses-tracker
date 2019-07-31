from django.shortcuts import render
from .models import Expense

# Create your views here.
def expense_view(request):
    obj = Expense.objects.get(all)
    context = { 'title':obj.title}
    return render(request, "expense/detail.html", context)
