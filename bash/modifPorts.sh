#!/bin/bash
chemin=${0::-13}
conf=$(cat ${chemin}modif.conf | cut -d " " -f 2)
if [ "$conf" == "1" ]
then
    if [ "$(($RANDOM % 10))" == "0" ]
    then
        echo 1
    else
        echo 0
    fi
else
    echo 1
fi

exit 0;