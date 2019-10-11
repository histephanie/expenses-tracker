from django.shortcuts import render, redirect
from .models import Expense, ExpenseCategory
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from datetime import datetime
from expenses.models import Expense, User, StoreCategoryLink
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
    # make a dict that by default has a None category for uncategorized expenses and
    # at index category which is an id from the database,
    # assign the value of a dict containing category name and an empty list for expenses
    categories = {
        None: {'name': 'uncategorized', 'expenses': [], 'id': None}
    }
    for category in cats:
        categories[category] = {'name': category.name, 'expenses': [], 'id': category.pk }

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

# takes an html string as an input, and returns a list of Expense model objects
def extract_expenses(html):
    soup = BeautifulSoup(html, 'html.parser')
    expenses = []
    trs = soup.findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        # ignores trs that dont contain tds
        # such as the table header
        if len(tds) < 4:
            continue

        expense_date = tds[0].text
        try:
            expense_date = datetime.strptime(expense_date, "%d.%m.%Y")
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

        expense = Expense(store=store, date=expense_date, amount=amount, user=None)

        expenses.append(expense)

    return expenses

def test_parse_email(request):
    html = ""
    with open('email.html', 'r') as file:
        html = file.read()

    sender = "stephanie.bogantes@gmail.com"
    # Check if the sender user exists in our system
    try:
        user = User.objects.get(email=sender)
    except:
        # we still return ok to mailgun to avoid them resending us the email
        print("user not found")
        return HttpResponse('OK')

    # get unique store names and their category
    links = StoreCategoryLink.objects.filter(user=user)
    #make  a dic that contains store as key and category as value
    link_dic = {}

    for link in links:
        link_dic[link.store] = link.category

    expenses = extract_expenses(html)
    for expense in expenses:
        if expense.store in link_dic.keys():
            expense.category = link_dic[expense.store]
    print(expenses)
    return HttpResponse(expenses)

# receives emails sent to mailgun
# the @csrf_exempt decorator disables csrf protection for this view
@csrf_exempt
def receive_email(request):
    if request.method == 'POST':
        sender    = request.POST.get('sender')
        body_html = request.POST.get('body-html', '')
        print("THIS HAPPENED!!!!!!")

        # Check if the sender user exists in our system
        try:
            user = User.objects.get(email=sender)
        except:
            # we still return ok to mailgun to avoid them resending us the email
            print("user not found")
            return HttpResponse('OK')

        # Extract all the expenses from the email
        expenses = extract_expenses(body_html)

        # Assign the correct user to each expense
        for expense in expenses:
            expense.user = user
            expense.save()

    # Returned text is ignored but HTTP status code matters:
    # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
    return HttpResponse('OK')

def categorize_expense(request):
    # handle errors early, return method not allowed if it's not a POST
    # request or the user is not authenticated. This helps keep the code
    # indented nicely
    if request.method != 'POST' or not request.user.is_authenticated:
        return HttpResponseNotAllowed(['POST'])

    #get id from the category selected from the dropdown menu
    category_id = request.POST.get("category_id")
    store = request.POST.get("store_name")
    next_url = request.POST.get('next_url', '/expenses')

    # find category in database
    category = ExpenseCategory.objects.get(pk=category_id)

    # get all expenses with the same name and belonging to the same user
    expenses = Expense.objects.filter(user=request.user, store=store)
    for expense in expenses:
        # then assing the same category to them
        expense.category = category
        expense.save()

    # find if a store cat link exists for this user and store...
    links = StoreCategoryLink.objects.filter(user=request.user, store=store)
    # ...if it does update cat and save
    if len(links) > 0:
        links[0].category = category
        links[0].save()
    # if it doesnt creat and new one and save
    else:
        link = StoreCategoryLink(user=request.user, store=store, category=category)
        link.save()

    return HttpResponseRedirect(next_url)
