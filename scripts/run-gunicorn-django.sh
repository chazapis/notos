#!/bin/bash
set -e
APPNAME=notos
PORT=8080
APPDIR=/srv/notos
LOGDIR=/var/log/gunicorn
LOGFILE=$LOGDIR/$APPNAME.log
USER=www-data
GROUP=www-data
NUM_WORKERS=2
cd $APPDIR
source $APPDIR/venv/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn $APPNAME.wsgi:application \
  -w $NUM_WORKERS -b 127.0.0.1:$PORT \
  --user=$USER --group=$GROUP \
  --settings=$APPNAME.settings.production \
  --timeout=600 --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE
exit 0
