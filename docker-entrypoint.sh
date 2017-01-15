#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput
logpath=/var/log/gunicorn
touch $logpath/gunicorn.log
touch $logpath/access.log
touch $logpath/error.log
tail -n 0 -f $logpath/*.log &

/usr/sbin/crond -l 8

echo Starting Gunicorn.
exec gunicorn eodassistant.wsgi \
    --name eod_assistant \
    --bind 0.0.0.0:8000 \
    --max-requests 30 \
    --threads 5 \
    --log-level=info \
    --log-file=$logpath/gunicorn.log \
    --error-logfile=$logpath/error.log \
    --access-logfile=$logpath/access.log \
    "$@"
