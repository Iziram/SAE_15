#!/bin/bash

date=$(date '+%s')

infos=$(netstat -nautA inet | tail -n +3 | tr -s ' ')

before=$IFS
IFS=$'\n'
for ligne in $infos
do
    socket_local=`echo $ligne | cut -d " " -f 4`
    socket_distant=`echo $ligne | cut -d " " -f 5`
    port_local=`echo $socket_local | cut -d ':' -f 2`
    port_distant=`echo $socket_distant | cut -d ':' -f 2`

    protocol="d"
    if (( port_local > 10000 ));
    then
       protocol=$port_distant
    else
       protocol=$port_local
    fi

    echo "$(echo $socket_local | cut -d ':' -f 1 ),$port_local,$protocol,$date"
done;
IFS=$before
exit 0;
