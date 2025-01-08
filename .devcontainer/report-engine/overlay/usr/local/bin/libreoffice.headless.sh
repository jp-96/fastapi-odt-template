#!/bin/bash
# libreoffice.org  headless server script
#
# chkconfig: 2345 80 30
# description: headless libreoffice server script
# processname: libreoffice
# 
# Author: Vic Vijayakumar
# Modified by Federico Ch. Tomasczik
# Modified by Manuel Vega Ulloa
# Modified by Sergey Podushkin
# Modified by Fábio Caritas Barrionuevo da Luz
# Baseado em: http://superuser.com/questions/542237/init-d-script-for-openoffice-libreoffice-headless-does-not-stop-process
#           GitHub Gist  https://gist.github.com/luzfcb/479fa8cb00bca50ecc6e

ACCEPT_HOST=0
ACCEPT_PORT=8997
PIDFILE=/var/run/libreoffice-server.pid
PID=`ps ax|grep "soffice.bin --headless"|grep -v grep|cut -d p -f 1`
set -e

case "$1" in
    start)
    if [ -f $PIDFILE ]; then
      echo "LibreOffice headless server has already started."
      sleep 5
      exit
    fi
      echo "Starting LibreOffice headless server"
      /usr/bin/libreoffice --nologo --norestore --invisible --headless --accept='socket,host=0,port=8997,tcpNoDelay=1;urp;' & > /dev/null 2>&1
      echo "LibreOffice headless server is running." > $PIDFILE
    ;;
    stop)
    if [ -f $PIDFILE ]; then
      echo "Stopping LibreOffice headless server. $PID"
      kill $PID
      rm -f $PIDFILE
      exit
    fi
      echo "LibreOffice headless server is not running."
      exit
    ;;
    *)
    echo "Usage: $0 {start|stop}"
    exit 1
esac
