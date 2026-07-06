web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn event_management.wsgi --bind 0.0.0.0:$PORT --log-file -
