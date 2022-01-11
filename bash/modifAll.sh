#!/bin/bash

chemin="${0::-11}modif.conf"

confs=$(<${chemin})
> ${chemin} 

for i in $confs
do
    if [ "$i" == "1" ]
    then
        echo -n "0 " >> $chemin
    else
        echo -n "1 " >> $chemin
    fi
done 

exit 0;
