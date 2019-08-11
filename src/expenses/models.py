from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return 'Category: ' + self.name

class Expense(models.Model):
    store    = models.CharField(max_length=120)
    date     = models.DateField(null=True)
    amount   = models.DecimalField(decimal_places=2, max_digits=10000, default=0)
    user     = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Expense: ' + self.store
