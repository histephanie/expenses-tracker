"""expensestracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from pages.views import signup_view, home_view
from expenses.views import expense_list_view, receive_email, test_parse_email, categorize_expense
import django.contrib.auth.urls

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('signup', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('expenses', expense_list_view, name='expenses'),
    path('categorize-expense', categorize_expense, name='categorize-expense'),
    path('expenses/<int:selected_year>-<int:selected_month>', expense_list_view, name='expenses'),
    path('api/receive-email', receive_email, name='email'),
    path('api/test-parse-email', test_parse_email, name='test-parse-email'),
]
