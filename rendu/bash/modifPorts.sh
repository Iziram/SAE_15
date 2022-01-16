#!/bin/bash

#On récupère le chemin pour pouvoir accéder au fichier de configuration.
chemin=${0::-13}

#On lit le fichier et on prend le deuxième chiffre qui s'y trouve, il correspond à un booléen disant si on doit ou non modifier les observations des ports.
conf=$(cat ${chemin}modif.conf | cut -d " " -f 2)

#Si le chiffre est à 1 cela veut dire que l'on doit modifier le port.
if [ "$conf" == "1" ]
then
    #La modification est pensée comme suit : il y a une chance sur 10 pour que le port qui devait être affiché ne s'affiche pas.
    if [ "$(($RANDOM % 10))" == "0" ]
    then
        #On sort 1 dans la sortie pour signifier que le port ne doit pas être affiché
        echo 1
    else
        #Sinon on sort 0.
        echo 0
    fi
else
    echo 1
fi

exit 0;