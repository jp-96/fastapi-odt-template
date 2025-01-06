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
#             GitHub Gist - https://gist.github.com/luzfcb/479fa8cb00bca50ecc6e

OOo_HOME=/usr/bin
SOFFICE_PATH=$OOo_HOME/soffice
PIDFILE=/var/run/libreoffice-server.pid
set -e

case "$1" in
    start)
    if [ -f $PIDFILE ]; then
      echo "LibreOffice headless server has already started."
      sleep 5
      exit
    fi
      echo "Starting LibreOffice headless server"
      $SOFFICE_PATH --headless --nologo --nofirststartwizard --    accept="socket,host=127.0.0.1,port=8100;urp" & > /dev/null 2>&1
      PID=`ps ax|grep "soffice.bin --headless"|grep -v grep|cut -d \  -f 1`
      echo $PID> $PIDFILE
    ;;
    stop)
    if [ -f $PIDFILE ]; then
      echo "Stopping LibreOffice headless server."
      kill `cat $PIDFILE`
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
