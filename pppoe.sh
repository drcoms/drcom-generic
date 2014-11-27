#!/bin/sh

server="127.0.0.1"

while(1)
do
    echo "Test connectivity to auth server"
    ping -c1 $server
    if [ $? != 0 ]
    then
        echo "ping failed, retry"
    else
        echo "OK"
        break
    fi
done

exec python /usr/bin/drcom-pppoe.py
