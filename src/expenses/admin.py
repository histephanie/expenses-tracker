from django.contrib import admin

# Register your models here.
from .models import Expense, ExpenseCategory, StoreCategoryLink
admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(StoreCategoryLink)
