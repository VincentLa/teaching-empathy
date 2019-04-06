web: gunicorn teaching_empathy.teaching_empathy.wsgi --log-file -
release: python teaching_empathy/manage.py migrate
web: python teaching_empathy/manage.py runserver 0.0.0.0:$PORT