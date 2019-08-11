Description:
This web-app enables people to send their Halkbank credit card expenses email to our app/website, and have the app automatically categorize expenses based on the store the expense was made in. If a store hasn’t been categorized yet, the user should be able to categorize it, and all current and future expenses from the same store should get (re)categorized under the selected category.
Projects organization:

Expenses Tracker
    .vscode
    src
        expensestracker
        expenses
        pages
        templates
            registration
    venv
    .gitignore
    README.md

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
