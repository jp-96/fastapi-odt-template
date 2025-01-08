from py3o.renderers.juno import start_jvm, Convertor, formats
import datetime

# /usr/bin/libreoffice --nologo --norestore --invisible --headless --accept='socket,host=0,port=8997,tcpNoDelay=1;urp;' &
# cd /opt/report-engine/code/example/py3o/
# python juno.py

# sudo apt-get update
# sudo apt-get install supervisor
# sudo supervisord

# sudo service supervisor restart
# sudo service supervisor status

# first arg is the jvm.so or .dll
# second arg is the basedir where we can find the basis3.3/program/classes/unoil.jar
# third argument it the ure basedir where we can find ure/share/java/*.jar containing
# java_uno.jar, juh.jar, jurt.jar, unoloader.jar
# the fourth argument was the openoffice version but is no more used
# fifth argument is the max memory you want to give to the JVM
start_jvm(
        # "/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server/libjvm.so",
        "/usr/lib/jvm/java-11-openjdk-amd64/lib/server/libjvm.so",
        "/usr/lib/libreoffice",
        "/usr/lib",
        "",
        140)
c = Convertor("127.0.0.1", "8997")

t1 = datetime.datetime.now()
c.convert("py3o_example.odt", "py3o_example.pdf", formats['PDF'])
t2 = datetime.datetime.now()
print(t1)
print(t2)
