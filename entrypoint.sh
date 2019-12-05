#!/bin/bash

set -e

#-------------------------------------------------------------------------------
# Handle shutdown/cleanup
#-------------------------------------------------------------------------------
function cleanup {
    if [ "Z$WAIT_PIDS" != "Z" ]; then
        kill -15 $WAIT_PIDS
    fi
}

# trap signals so we can shutdown sssd cleanly
trap cleanup HUP INT QUIT TERM

#-------------------------------------------------------------------------------
# configure supervisor
#-------------------------------------------------------------------------------
cat <<END >| /etc/supervisord.conf
[supervisord]
nodaemon=true
logfile=/tmp/supervisord.log
pidfile=/tmp/supervisord.pid


[program:thelma]
directory=/srv/thelma/app/thelma
command=gunicorn --pid /srv/thelma/thelma.pid --bind 0.0.0.0:8002 -w ${WORKERS} -e DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} --access-logfile - --error-logfile - --log-level trace config.wsgi:application
stdout_logfile=/srv/thelma/app/thelma.log
stdout_logfile_maxbytes=0
stderr_logfile=/srv/thelma/app/thelma.err
stderr_logfile_maxbytes=0
END

rm -f /srv/thelma/thelma.pid
python manage.py collectstatic --no-input --link --clear
if test -t 0; then
    /usr/bin/supervisord -c /etc/supervisord.conf &
    WAIT_PIDS=$!
    if [[ $@ ]]; then
        eval $@
    fi
    wait $WAIT_PIDS
else
    /usr/bin/supervisord -c /etc/supervisord.conf
fi
