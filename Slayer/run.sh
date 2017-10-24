python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn --bind 0.0.0.0:8001 --workers 3 --timeout 120 --worker-class gevent --log-level=INFO --access-logfile - --error-logfile - --user 0 --group 0 Slayer.wsgi 