from django.shortcuts import render, redirect
from .models import Expense, ExpenseCategory
from datetime import datetime, date, timedelta
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# This view shows a list of all expenses made by the user in the current month
# unless a specific month was requested
def expense_list_view(request, selected_year=None, selected_month=None):
    # verify if user is logged in, otherwise redirect to log in page
    if not request.user.is_authenticated:
        return redirect('login')

    # by default, look at the current month
    selected_timeframe = datetime.now()

    # if a specific timeframe was requested, set our timeframe to that
    if selected_year is not None and selected_month is not None:
        # get the month/year from the slug
        selected_timeframe = datetime.strptime(f"{selected_year}-{selected_month}", "%Y-%m")

    month_text = selected_timeframe.strftime('%B')
    current_month_slug = selected_timeframe.strftime('%Y-%m')
    # take selected date and replace it with the first day of that month
    # eg. Aug 13th, 2019 becomes Aug 1st, 2019
    first = selected_timeframe.replace(day=1)
    # take the first day of the month and subtract one more day
    # taking you back to the previous month
    prev_month = (first - timedelta(days=1)).strftime('%Y-%m')

    last = selected_timeframe.replace(day=28)

    if selected_timeframe.year == datetime.now().year and selected_timeframe.month == datetime.now().month:
        next_month = datetime.now().strftime('%Y-%m') # this becomes DateTime(year=2019,month=08,day=14)
    else:
        next_month = (last + timedelta(days=4)).strftime('%Y-%m') # eg. "2019-08"

    year = selected_timeframe.strftime('%Y')
    month = selected_timeframe.strftime('%m')
    expenses = Expense.objects.filter(user=request.user, date__year=year, date__month=month)

    #dropdown menu list
    nav_months = [selected_timeframe]
    #everytime you select a month, it becomes the reference month
    ref_month = selected_timeframe
    for i in range(4):
        # go back to the first day of the ref month
        first = ref_month.replace(day=1)
        # go back one more day to get to the privious month
        ref_month = first - timedelta(days=1)
        # append the ref month to end up with a list of 4 months from the selected time frame
        nav_months.append(ref_month)
    nav_months.reverse()

    present_month = datetime.now()
    ref_month = selected_timeframe
    for i in range(4):
        # go back to the first day of the ref month
        last = ref_month.replace(day=28)
        # go back one more day to get to the privious month
        ref_month = last + timedelta(days=4)

        # if ref month is later than our present month, stop adding
        if ref_month > present_month:
            break

        # append the ref month to the list of navigation months
        nav_months.append(ref_month)


    print(nav_months)

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
        'nav_months': nav_months,
        'selected_timeframe': selected_timeframe,
    }
    return render(request, "expense-list.html", context)

# receives emails sent to mailgun
# the @csrf_exempt decorator disables csrf protection for this view
@csrf_exempt
def receive_email(request):
    if request.method == 'POST':
        sender    = request.POST.get('sender')
        recipient = request.POST.get('recipient')
        subject   = request.POST.get('subject', '')
        body_html = request.POST.get('body-html', '')
        body_without_quotes = request.POST.get('stripped-text', '')

        #### SAVE body_html to a file
        with open("email.html", "w") as text_file:
            text_file.write(body_html)

        # note: other MIME headers are also posted here...

        # attachments:
        for key in request.FILES:
            file = request.FILES[key]
            # do something with the file

    # Returned text is ignored but HTTP status code matters:
    # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
    return HttpResponse('OK')
