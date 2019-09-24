# Expense Tracker

This web-app enables people to send their Halkbank credit card expenses email to our app/website, and have the app automatically categorize expenses based on the store the expense was made in. If a store hasn’t been categorized yet, the user should be able to categorize it, and all current and future expenses from the same store should get (re)categorized under the selected category.
Project organization:

```
Expenses Tracker
    .vscode
    src
        expensestracker
        expenses
        pages
        templates
            registration
        manage.py
    venv
    .gitignore
    README.md
```

venv instructions:
to create the virtual environment cd to your project's folder (expenses tracker) and run `python -m venv <venv name>` and activate it with `. <venv name>/bin/activate`


For the login, logout, signup, and user we've used the django built-in libraries.
Here're some simple tutorials:

login/logout:
https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/

signup:
https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

Make sure to costumize the redirect URL in settings.py as well as the redirect for the signup view

We've used bootstrap 4 for the front-end.

# Test Receiving Email from Mailgun:

## Quick and Simple Test
1. start up the local sever `python manage.py runserver`
2. start an ngrok tunnel `ngrok http 8000`
3. log in to mailgun and select "Receiving" from the menu on the left
4. Enter the URL you got from ngrok and append the receive email route `/api/receive-email` and hit POST

At this point you should see a success message from mailgun. Now that you've made sure the simple test is successful, you can run a full test with a real email.

## Full Email Test
1. In your list of routes in mailgun, edit the catch_all route.
2. Set the forward URL to your ngrok url and append `/api/receive-email`, then save.
3. Forward the email you received from Halkbank to `expenses@sandboxf44eff04716248648a90336077b7a6ac.mailgun.org`
