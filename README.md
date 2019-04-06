# teaching-empathy
Teaching Empathy Through Social Learning and Virtual Pen Pal Relationships

Guide: https://medium.com/python-pandemonium/building-and-deploying-an-enterprise-django-web-app-in-16-hours-79e018f7b94c
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/skeleton_website

## Development Environment

1. First install Python

Create a Python Environment:

```
pyenv virtualenv 3.6.2 teaching-empathy
```

To activate this environment:

```
pyenv activate teaching-empathy
```

Remember, after making changes to model, need to perform migrations:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

To run:

```
python3 manage.py runserver
```

As of 2019-02-25, finished building Models: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
Next, https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site

Creating a super user: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site#Creating_a_superuser

```
python3 manage.py createsuperuser
```

Username: vincentla
email: vincent@teachingempathy.com
password: teachingempathy

## Login Page Tutorial
https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/ -- Buggy
https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

## Messages
Bootstrap Alerts: https://getbootstrap.com/docs/3.3/components/

## To Deploy to Heroku
In Heroku:

1. Git Push to the repository like you normally would.
2. Push to Heroku `git push heroku master`
3. Go to https://teachingempathy.herokuapp.com/pen_pal/ to see the App!

```
heroku run python teaching_empathy/manage.py migrate
```
