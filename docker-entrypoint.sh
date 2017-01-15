#!/usr/bash

python manage.py migrate
python manage.py collectstatic --noinput

touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
touch /srv/logs/error.log
tail -n 0 -f /srv/logs/*.log &

echo Starting Gunicorn.
exec gunicorn eodassistant.wsgi \
    --name eod_assistant \
    --bind 0.0.0.0:80 \
    --max-requests 30 \
    --threads 5 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --error-logfile=/srv/logs/error.log \
    --access-logfile=/srv/logs/access.log \
    "$@"
