#!/bin/bash
if [ $# -gt 1 ]
then
    chemin=${0::-20}
    
    conf=$(cat ${chemin}modif.conf | cut -d " " -f 1)
    if [ "$conf" == "1" ]
    then
        if [ "$1" == "ping" ]
        then
            rdm=$((1 + $RANDOM % 500))
            val=$(bc <<< $rdm+"$2");
            echo $val;
        else
            rdm=$((-200 + $RANDOM % 600))
            val=$(bc <<< $rdm+$2);
            echo ${val#-}
        fi
    else
        echo $2
    fi
fi
exit 0;