APPNAME=hackathon
APPDIR=/home/ubuntu/hackathon-website/hackathon
LOGFILE='$APPDIR/gunicorn.log'
ERRORFILE='$APPDIR/gunicorn-error.log'

NUM_WORKERS=3

ADDRESS=127.0.0.1:8000

cd $APPDIR
source ~/.bashrc
workon $APPNAME

exec gunicorn $APPNAME.wsgi:application \
	-w $NUM_WORKERS --bind=$ADDRESS \
	--log-level=debug \
	--error-logfile $ERRORFILE \
	--access-logfile $LOGFILE &
